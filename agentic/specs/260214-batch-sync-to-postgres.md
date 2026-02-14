# Chore: Batch sync-to-postgres upserts for 20-30x speedup

## Metadata

run_id: `8c014937`
prompt: `https://github.com/MarkusNeusinger/pyplots/issues/4170`

## Chore Description

The `Sync: PostgreSQL` GitHub Actions workflow takes ~18 minutes to complete. The bottleneck is the `sync_to_database()` function in `automation/scripts/sync_to_postgres.py`, which executes 2,426 individual INSERT...ON CONFLICT DO UPDATE queries against Cloud SQL, each with ~420ms network round-trip latency.

The fix involves batching these upserts so that instead of 2,426 round-trips, we make ~7 (libraries batch + spec chunks + impl chunks + cleanup queries). Additionally, the workflow runs with `ENVIRONMENT` defaulting to `"development"`, causing `echo=True` on the SQLAlchemy engine — logging all 9,770+ SQL lines unnecessarily.

Expected improvement: ~18 minutes → ~30-60 seconds.

## Relevant Files

Use these files to complete the chore:

- **`automation/scripts/sync_to_postgres.py`** — Main sync script. The `sync_to_database()` function (lines 355-470) is the target for batching. Currently executes individual `session.execute(stmt)` calls per spec and per implementation.
- **`core/database/connection.py`** — Database connection setup. Contains `echo=ENVIRONMENT == "development"` (line 85) for Cloud SQL engine. The workflow doesn't set `ENVIRONMENT`, so it defaults to `"development"` and logs all SQL.
- **`.github/workflows/sync-postgres.yml`** — Workflow file. Needs `ENVIRONMENT: production` added to the sync step env vars to disable SQL echo logging.
- **`core/database/models.py`** — Defines `Spec`, `Impl`, `Library` models. The `Impl` table has a `UniqueConstraint("spec_id", "library_id", name="uq_impl")` used for ON CONFLICT.
- **`tests/unit/automation/scripts/test_sync_to_postgres.py`** — Unit tests for the sync script. The `TestSyncToDatabase` class (lines 656-813) uses `MagicMock` sessions and must be updated to reflect the new batched approach.

## Step by Step Tasks

IMPORTANT: Execute every step in order, top to bottom.

### 1. Add ENVIRONMENT variable to the workflow

- In `.github/workflows/sync-postgres.yml`, add `ENVIRONMENT: production` to the env block of the "Sync plots to database" step (line 62-68)
- This disables `echo=True` on the SQLAlchemy engine, eliminating ~9,770 log lines per run

### 2. Batch library seed inserts

- In `sync_to_database()`, replace the library seed loop (lines 369-371) with a single batched insert
- Collect all `LIBRARIES_SEED` values and execute one `insert().on_conflict_do_nothing()` with multiple values
- Use `session.execute(stmt, lib_data_list)` pattern or build a single multi-row insert statement

### 3. Batch spec upserts with chunking

- Replace the individual spec upsert loop (lines 382-403) with chunked batch execution
- Collect all spec values into a list, then execute in chunks of 500
- For each chunk, build a single `insert(Spec).values(spec_values_list).on_conflict_do_update(...)` statement
- This reduces ~257 round-trips to 1 round-trip

### 4. Batch implementation upserts with chunking

- Replace the individual impl upsert loop (lines 406-448) with chunked batch execution
- Build impl values with all fields (including optional fields and review data) pre-computed
- For the ON CONFLICT update set, use `insert(Impl).excluded` to reference the incoming values
- Execute in chunks of 500 rows, reducing ~2,160 round-trips to ~5 round-trips
- The `on_conflict_do_update` must reference constraint `"uq_impl"` and set all fields from the excluded row

### 5. Batch implementation deletions

- Replace the individual impl delete loop (lines 464-465) with a single batched delete
- Instead of looping through `removed_impls` and executing one DELETE per pair, use a single DELETE with a compound IN clause: `WHERE (spec_id, library_id) IN (list_of_tuples)`
- Use SQLAlchemy's `tuple_()` construct to build the compound condition

### 6. Add helper function for chunked execution

- Create a small helper function `_chunked(iterable, size)` to split lists into chunks of a given size
- Use chunk size of 500 (safe for PostgreSQL's parameter limit while still providing massive batching benefit)

### 7. Update unit tests for batched sync

- Update `TestSyncToDatabase` tests to account for the new batched execution pattern
- The mock session's `execute` will now be called fewer times (batched calls instead of per-row calls)
- Verify that `session.commit()` is still called exactly once
- Verify stats counters still report correct counts
- Add a test with multiple specs and impls to verify chunking behavior

### 8. Validate the implementation

- Run the unit test suite to ensure all tests pass
- Run lint checks to ensure code quality

## Validation Commands

Execute these commands to validate the chore is complete:

- `uv run python -m py_compile automation/scripts/sync_to_postgres.py` — Verify the script compiles
- `uv run pytest tests/unit/automation/scripts/test_sync_to_postgres.py -v` — Run all unit tests for the sync script
- `uv run ruff check automation/scripts/sync_to_postgres.py` — Lint the modified script
- `uv run ruff check .github/workflows/sync-postgres.yml` — Verify workflow YAML (ruff won't lint YAML, but no syntax errors)

## Notes

- The `insert(Impl).values(list_of_dicts)` pattern with `on_conflict_do_update` using `excluded` is supported by SQLAlchemy's PostgreSQL dialect. The `excluded` pseudo-table references the row that would have been inserted.
- Chunk size of 500 is chosen because PostgreSQL has a per-query parameter limit (~32,767 parameters). With ~25 columns per impl row, 500 rows × 25 params = 12,500 parameters — well within limits.
- The `ENVIRONMENT: production` change is safe because the workflow only runs in GitHub Actions against the production database. The sync script's own logger still logs at INFO level, providing adequate visibility.
- The spec upserts must execute before impl upserts due to FK constraints (`impls.spec_id → specs.id`). Within each batch, order doesn't matter since all specs already exist or are being upserted.
- Library seed inserts use `on_conflict_do_nothing` (not update), so batching is even simpler.
