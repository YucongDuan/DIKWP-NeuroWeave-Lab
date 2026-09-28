# Contributing

Make one mechanism or one evaluation claim easier to inspect. A contribution should
state its assumptions, input/output contract, expected behavior, failure conditions,
and appropriate evidence domain. Include tests and an example that can fail when
the proposed mechanism is removed. Do not use a higher version number as evidence
of a stronger scientific claim.

Run `python -m unittest discover -s tests -v` before submitting a change. Then run
`python scripts/reproduce.py --out outputs/reproduced`. A deliberate algorithm change
will alter reference results; explain the change, update its protocol version, and
regenerate rather than silently replacing expected results to make a test pass.

All new runtime functionality must preserve the label-free prediction boundary,
strict denominator accounting, visible uncertainty, source-history retention, and
explicitly declared execution scope. Never add downloaded or user-provided code to
an executable rule registry without human code review. Text adapters must produce
reviewable candidate claims, not grants of authority.

The core deliberately uses the standard library. Optional integrations should be
separate extras with their own tests and licensing. Adding an integration stub does
not justify listing the integration as supported. Document computational cost and
changes to the threat model. Keep documentation, UI strings and examples in English.

Book authorship, framework attribution and implementation authorship are different.
Preserve accurate credits. Name a confirmed maintainer and real repository URL when
publishing; the distributed package does not invent either.
