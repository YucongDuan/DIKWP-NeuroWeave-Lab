"""Transactional, hash-linked event log. Tamper-evident, not tamper-proof.

An externally retained expected head detects truncation/full replacement. Without
it, a privileged writer can rewrite the entire chain or remove its suffix.
"""
from __future__ import annotations
import json
import sqlite3
import threading
from pathlib import Path
from .util import canonical, digest, nonempty

GENESIS = "0" * 64


class IntegrityError(ValueError):
    """An event chain is inconsistent with its content or trusted checkpoint."""


class ConflictError(RuntimeError):
    """Another writer advanced the log; reload state before retrying."""


class Ledger:
    def __init__(self, path: str | Path = ":memory:") -> None:
        self.lock = threading.RLock()
        self.connection = sqlite3.connect(str(path), timeout=5, check_same_thread=False)
        with self.connection:
            self.connection.execute("CREATE TABLE IF NOT EXISTS events (seq INTEGER PRIMARY KEY, kind TEXT NOT NULL, payload TEXT NOT NULL, prev TEXT NOT NULL, hash TEXT NOT NULL)")
        self.verify()

    def events(self) -> list[dict]:
        with self.lock:
            rows = self.connection.execute("SELECT seq,kind,payload,prev,hash FROM events ORDER BY seq").fetchall()
        return [dict(seq=r[0], kind=r[1], payload=json.loads(r[2]), prev=r[3], hash=r[4]) for r in rows]

    @property
    def head(self) -> str:
        with self.lock:
            row = self.connection.execute("SELECT hash FROM events ORDER BY seq DESC LIMIT 1").fetchone()
            return row[0] if row else GENESIS

    def verify(self, expected_head: str | None = None) -> str:
        prev = GENESIS
        try:
            for seq, e in enumerate(self.events(), 1):
                core = {k: e[k] for k in ("seq", "kind", "payload", "prev")}
                if e["seq"] != seq or e["prev"] != prev or digest(core) != e["hash"]:
                    raise IntegrityError(f"Invalid ledger entry at sequence {seq}")
                prev = e["hash"]
        except (json.JSONDecodeError, TypeError, OverflowError) as exc:
            raise IntegrityError("Invalid ledger payload") from exc
        if expected_head is not None and prev != expected_head:
            raise IntegrityError("Ledger differs from expected checkpoint")
        return prev

    def append(self, kind: str, payload: dict, *, expected_head: str | None = None) -> dict:
        nonempty(kind, "kind")
        text = canonical(payload)
        with self.lock:
            try:
                self.connection.execute("BEGIN IMMEDIATE")
                self.verify()
                row = self.connection.execute("SELECT seq,hash FROM events ORDER BY seq DESC LIMIT 1").fetchone()
                seq, prev = (row[0] + 1, row[1]) if row else (1, GENESIS)
                if expected_head is not None and expected_head != prev:
                    raise ConflictError("Concurrent state change; construct a fresh Memory and retry")
                core = dict(seq=seq, kind=kind, payload=json.loads(text), prev=prev)
                hash_ = digest(core)
                self.connection.execute("INSERT INTO events VALUES (?,?,?,?,?)", (seq, kind, text, prev, hash_))
                self.connection.commit()
                return dict(core, hash=hash_)
            except BaseException:
                self.connection.rollback()
                raise

    def close(self) -> None:
        self.connection.close()
