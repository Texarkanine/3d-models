# Progress

An update deploy must select the Cults design whose `creation.id` is the stored `cults_creation_id`, including when that design is not the newest, and must fail when the read returns a different design.

**Complexity:** Level 1

## 2026-10-19 - COMPLEXITY-ANALYSIS - COMPLETE

* Work completed
    - Compared the 15 October and 19 October Cults schemas: 84 types, no signature change
    - Confirmed `creationsBatch(ids:)` filters on `creation.identifier` and that a slug returns every design
    - Classified the publisher fix as Level 1
* Decisions made
    - The stored id stays `creation.id`, the value `updateCreation` documents
    - The lookup stops using `creationsBatch(ids:)`
* Insights
    - The slug and padding fixes succeeded when the target was the only design or the newest one, because `limit: 1` returns that first row
