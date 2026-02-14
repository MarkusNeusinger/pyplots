# Batch Sync-to-Postgres Upserts

**Run ID:** 8c014937
**Date:** 2026-02-14
**Specification:** agentic/specs/260214-batch-sync-to-postgres.md

## Overview

Refactored the PostgreSQL sync script to use batched upserts instead of individual per-row INSERT...ON CONFLICT queries, reducing ~2,426 database round-trips to ~5. Also set `ENVIRONMENT: production` in the GitHub Actions workflow to disable verbose SQL echo logging. Expected improvement: ~18 minutes down to ~30-60 seconds.

## What Was Built

- Batched library seed inserts into a single multi-row `INSERT...ON CONFLICT DO NOTHING`
- Chunked spec upserts (500 rows per chunk) using `INSERT...ON CONFLICT DO UPDATE` with `excluded` references
- Chunked implementation upserts (500 rows per chunk) with the same pattern
- Batched implementation deletions using `tuple_().in_()` instead of per-row DELETE
- `_chunked()` helper generator for splitting iterables into fixed-size chunks
- `ENVIRONMENT: production` env var in the sync workflow to suppress SQL echo logging
- New unit tests covering the chunked helper and batched sync behavior

## Technical Implementation

### Files Modified

- `automation/scripts/sync_to_postgres.py`: Replaced per-row upsert loops with batched `insert().values(list).on_conflict_do_update()` using `stmt.excluded` references; added `_chunked()` helper, `_BATCH_CHUNK_SIZE` constant, and `_IMPL_UPDATE_FIELDS` list
- `.github/workflows/sync-postgres.yml`: Added `ENVIRONMENT: production` to the sync step env block
- `tests/unit/automation/scripts/test_sync_to_postgres.py`: Added `TestChunked` test class, added `impl_tags` field to existing test fixtures, added `test_sync_batches_multiple_specs_and_impls` test verifying batched execute call count

### Key Changes

- All spec/impl values are now collected into lists before any database calls, then upserted in chunks of 500 rows
- The `on_conflict_do_update` `set_` dict is built dynamically from `stmt.excluded[field]`, eliminating per-row conditional field logic
- Removed the per-implementation loop that conditionally added optional fields — all fields are now always included in the batch values
- Implementation deletions use `tuple_(Impl.spec_id, Impl.library_id).in_(removed_impls)` for a single DELETE statement
- Stats counters are set from list lengths instead of being incremented per row

## How to Use

1. No usage changes — the sync script is called the same way via `uv run python automation/scripts/sync_to_postgres.py`
2. The GitHub Actions workflow (`sync-postgres.yml`) triggers automatically and now runs significantly faster
3. SQL echo logging is suppressed in CI; to debug SQL locally, ensure `ENVIRONMENT` is not set or set to `development`

## Configuration

- `_BATCH_CHUNK_SIZE = 500` — Controls the number of rows per batched INSERT. Safe for PostgreSQL's ~32,767 parameter limit with ~25 columns per row
- `ENVIRONMENT: production` — Set in `.github/workflows/sync-postgres.yml` to disable SQLAlchemy `echo=True`

## Testing

```bash
uv run pytest tests/unit/automation/scripts/test_sync_to_postgres.py -v
```

Key test additions:
- `TestChunked` — Validates exact division, remainder, empty input, single element, and oversized chunk
- `test_sync_batches_multiple_specs_and_impls` — Verifies that 5 specs with 3 impls each result in only 5 `session.execute` calls (1 library seed + 1 spec chunk + 1 impl chunk + 2 removal selects) vs 22 in the old per-row approach

## Notes

- The raincloud-basic plot files also changed in this diff but are unrelated to the sync batching feature
- The `_IMPL_UPDATE_FIELDS` list must be kept in sync with the `Impl` model columns if new fields are added
- Chunk size of 500 is conservative; could be increased if the number of columns stays stable
