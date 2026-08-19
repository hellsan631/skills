# Migration plan

## Goals

- **Correctness:** No record may be dropped during the cutover.
- **Reversibility:** Every step must roll back within ten minutes.
- **Observability:** Row counts get compared after each batch.
- **Cost:** The read replica stays on the existing instance class.

## Phases

- **Phase 1:** Stand up the replica and verify replication lag.
- **Phase 2:** Backfill historical rows in batches of fifty thousand.
- **Phase 3:** Switch reads to the replica behind a flag.
- **Phase 4:** Switch writes and retire the old table.
- **Phase 5:** Drop the compatibility shim.

## Risks

- Replication lag spikes during the backfill window.
- The compatibility shim hides a schema mismatch until phase four.
- Batch size interacts badly with the nightly vacuum.
- Rollback after phase four requires a full restore.
- On-call coverage is thin during the planned window.
- The staging dataset is four months stale.

## Owners

- Backfill tooling sits with the platform team.
- Flag rollout sits with the application team.
- Restore rehearsal sits with the database group.
