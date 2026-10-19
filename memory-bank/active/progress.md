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

## 2026-10-19 - BUILD - COMPLETE

* Work completed
    - The test double no longer treats `ids` as a slug filter
    - An update whose stored id is not the newest design selects that design
    - A page that contains only a different design stops before `updateCreation`
    - Catalog suite: 82 tests passed
* Decisions made
    - Find the row by `creation.id` across the unfiltered account list
    - Do not store or send `creation.identifier`
* Insights
    - `limit: 1` on an unfiltered list made the newest design look like a successful lookup
