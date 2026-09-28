# Security and execution boundary

This release is a single-user local teaching application, not a security boundary
against a hostile user of the same computer. The HTTP server binds only to
127.0.0.1. It accepts a fixed set of static routes and a bounded JSON experiment API.
Requests with a non-loopback Host, a cross-origin browser Origin, or unsupported
parameters are rejected. Arbitrary paths, executable expressions, shell commands,
cloud credentials and external actuators are not accepted by the API.

The server uses Python's standard-library HTTP implementation, which is not a
production web service. Do not expose it with a reverse proxy or public tunnel.
There is no account system, TLS, rate limiter, application sandbox, or multi-tenant
isolation. A local process can issue requests without an Origin header. Browser
checks are not a replacement for authentication. There is no CSRF token because
there is no authenticated remote mutation API; same-origin JSON and Host checks
protect the intended loopback experiment surface only.

Consent owners and timestamps are supplied by the local teaching process, not
verified human identities or trusted clocks. Pending plans and consent states are
in memory and intentionally disappear at process shutdown. Do not attach a real
actuator or interpret a session receipt as human consent without independently
implementing authentication, durable authorization, trusted time and deployment review.

The SQLite ledger detects inconsistent links and content hashes. A locally retained
expected head detects suffix deletion or replacement. A privileged writer who can
replace both the log and its checkpoint can forge a new consistent history.
There is no digital signature, timestamp authority, consensus, encryption at rest,
or append-only storage hardware. Source fields are declarations, not authenticated URLs.

Memory persistence is transactional within its dedicated log. The unified runtime's
consent state, resource debit and feedback write are not one durable distributed
transaction. A disk-write failure during a synthetic execution requires inspection
of the session audit and remaining budget; retrying the same ID is not permitted.
Only local simulations exist, so no real-world rollback is claimed.

For sensitive information use a separately designed privacy and retention system.
The append-only source history deliberately retains earlier values; logical withdrawal
does not erase SQLite pages, backups or released files. This release bundles no human
records and is not intended as a repository for patient or private neural data.

Before adapting for untrusted input, add input contracts appropriate to the adapter,
resource isolation, event-size limits, durable recovery, dependency/schema versioning,
and a threat-model-specific security review. Report a vulnerability to the maintainer
of the repository where this package is eventually published; no monitoring channel
or response-time promise is implied by this delivery.
