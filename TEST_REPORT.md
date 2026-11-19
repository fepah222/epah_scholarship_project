# Epah Scholarship verification report

## Source and consistency checks

- Reviewed the supplied project archive, including all Python models, routes, sockets, templates, CSS/JavaScript, configuration, setup scripts, tests and project specifications.
- Replaced implicit SQLAlchemy table naming with explicit names for all 29 documented tables.
- Added a database uniqueness constraint preventing duplicate applications by the same student to the same scholarship.
- Confirmed the documented foreign-key names now have matching model table declarations by static source analysis.
- Updated application identity and the default SQLite database name to Epah Scholarship / `epah_scholarship.db`.
- Added schema regression tests for all 29 tables and every foreign-key target.
- Updated Windows setup scripts to recognize Python 3.12–3.15 and to run dependency checks and tests.
- Excluded `.env`, local databases, virtual environments, IDE state and caches from the release archive.

## Runtime test status

Python syntax compilation and archive integrity checks are performed during packaging. Full Flask/SQLAlchemy runtime tests could not be executed in the build environment because the package index was unreachable and the bundled Windows virtual-environment binaries are not compatible with this Linux test runtime. The installer runs `pip check` and `pytest` on the user's Windows machine and stops if either fails. Therefore this report does not claim that a live browser session has been verified here.

## Known limitations

See the README section “Known functional limitations”. This release corrects the supplied codebase and database model graph; it does not claim that the listed unimplemented workflows are complete.
