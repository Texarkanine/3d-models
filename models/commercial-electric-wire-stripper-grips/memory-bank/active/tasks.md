# Task: wire-stripper-grips-closed-end (rework: the pair that fits, ready to publish)

* Task ID: wire-stripper-grips-closed-end
* Complexity: Level 2
* Type: rework (simple enhancement, then publishing clean-up)

The operator printed both closed ends on both grips. The pair that fits the way the original grips did is curved grip iteration 5 (`e1b3528`) and straight grip iteration 2 (`a61aa6d`). One source must build exactly that pair. Then the model is made ready to publish: the publish record is filled out and the model directory describes only the two grips that ship (projectbrief "Rework (2026-11-02)").

## Design: the closed end per grip

A design value in `grips.py`, beside the other closed-end values:

```python
END_CLEAR = {"curved": 1.0, "straight": None}
```

- **A length (curved):** the bore runs that far past A at full width, as over a square tip. A gable rises from the corners of that end section, at `ROOF_ANGLE` in print, to a `RIDGE_W` strip at the apex. This is the code of `5d73490`, kept as it was: the same section positions, the same planes, the same order of operations. Then the STL comes out byte for byte the same.
- **`None` (straight):** the roof sits on the steel's rounded tip (`steel.Handle.tip_r`), as built in `a61aa6d`.
- **Shared behaviour:**
    - The ribs run at full height to `s_full`, then fade to the wall by `s_end`.
        - Length: `s_full = 0`, `s_end = −END_CLEAR`. These are `5d73490`'s positions exactly, since `loft_positions(L, 0.0)` ends at 0.0.
        - `None`: `s_full = tip_r + RIB_FADE`, `s_end = tip_r`.
    - The dome starts at `−past` in both. For a length, `past = END_CLEAR + rise`; `−(a + b)` is bitwise `−a − b`, so the dome's sections match `5d73490`'s.
- **Functions:**
    - `tip_roof(h)` is today's `roof(h)` → `(rows, past, ridge)`.
    - `gap_roof(h)` is `5d73490`'s `roof(h)` → `(r, rise)`.
    - `closed_end(h)` → `(past, ridge)` serves `outside()`, `sizes()` and the checks.
    - `bore()` and `ribs()` branch on `END_CLEAR[h.name]`.
- **The curved tip's reading** (`TIP_R` 1.5) stays in `steel.py`. It is a reading, but the curved grip's bore runs past the tip and does not use it. The docs say so.

## Test Plan (TDD)

The model's standing direction is scratch checks in `.scratch/wirestripper-grip/`, each printing PASS or FAIL with its exit code; `check_design` holds the parameter guards; the catalog suite guards the record.

### Behaviors to Verify

- **R1. The pair, byte for byte** (`pair_check.py`, new). The model's files equal the chosen iterations:
    - `curved_grip.stl` and `curved_grip_fit_test.stl` equal `baseline/*-iter5.stl` (`e1b3528`) byte for byte;
    - `straight_grip.stl` and `straight_grip_fit_test.stl` equal `baseline/*-iter2.stl` (`a61aa6d`) byte for byte;
    - each STEP file equals its baseline (`*-5d73490.step`, `*-a61aa6d.step`) apart from the `FILE_NAME` header line.

    Red now: the curved files are iteration 6.
- **R2. Parameter guards** (`design_guards.py`, adapted):
    - shipped parameters pass on both grips;
    - `END_CLEAR` 0 or negative on the curved grip raises;
    - the tip-radius guards and `ROOF_ANGLE` 44 raise;
    - the lean guard still fires for a leaning grip seated on its tip: the curved grip with `END_CLEAR` set to `None` and `ROOF_ANGLE` 80;
    - a square tip on the straight grip still builds (ridge 4.32).

    Red now: no `END_CLEAR` guard.
- **R3. The size report matches the grip built** (`report_check.py`, adapted):
    - the curved table's last row is "at A", with ribs. A length-closed grip has a full-width bore and full ribs at A.
    - the straight table's last row is "round starts", with no ribs;
    - each grip's closed-end line describes its own closed end.

    Red now: the curved table shows "round starts".
- **R4. The model checks hold for each closed end** (`verify.py`, mode-aware):
    - Both grips: no steel in the bore wall, the rib-bite rows, the thinnest wall, and the fit test equal to its grip cut at `FIT_LEN`.
    - Straight: the hug checks as before.
    - Curved: the cap over the apex is `DOME_LEN`; the rib bite is 8 ribs over L, as `5d73490` measured; no hug check.
- **R5. Unchanged checks:**
    - `closed_end.py` for the straight grip (2.30, 3.028 lower than iteration 1). The curved grip's ridge is 4.66 past A, as iteration 5.
    - `roof_angles.py`, `lip.py`, `corner_bevel.py`, `tools/overhang.py`, `shut_gap.py`, `tip_check.py`.
- **R6. The publish record** (catalog suite):
    - `test_every_listed_printable_exists` covers every file named in `publish.yaml`;
    - 88 OK.
- **Edge cases:**
    - `END_CLEAR` missing a handle's name: `KeyError` at once, not a silent default.
    - A curved `TIP_R` that no grip uses still passes the tip guard (0 ≤ 1.5 ≤ W/2).

### Test Infrastructure

- As the last run: scratch scripts in `.scratch/wirestripper-grip/`, and the catalog `unittest` suite in `tests/`.
- New: `pair_check.py`. Adapted: `design_guards.py`, `report_check.py`, `verify.py`, `closed_end.py`.

## Implementation Plan

### 1. The pair from one source (executable)

- Files:
    - `grips.py`;
    - the eight output files (the curved four return to iteration 5; the straight four stay);
    - the scratch checks above.

1. **Stub tests:** an empty `pair_check.py`; empty mode sections in `design_guards.py`, `report_check.py`, `verify.py` and `closed_end.py`.
2. **Stub interface:** `END_CLEAR` (dict); `gap_roof(h)` and `closed_end(h)` with docstrings, empty; `roof` renamed `tip_roof`.
3. **Write tests and run red:** R1 to R4 fail on the current files and code.
4. **Write code and run green:**
    - `gap_roof` is `5d73490`'s `roof`, verbatim.
    - `bore()`: for a length, `5d73490`'s body and cap, verbatim; for `None`, today's.
    - `ribs()` with `s_full` and `s_end`.
    - `outside()` uses `closed_end`.
    - `check_design`: `END_CLEAR[h.name]` is `None` or above 0; `tip_roof` only for `None`.
    - `sizes()`: the last row and the closed-end line per grip.
    - The docstring describes both closed ends.
    - Rebuild. Green: R1 to R5. Commit as the printable pair: `chore: saving progress on wire-stripper-grips-closed-end`. Its body names curved iteration 5 and straight iteration 2, and says they fit like the originals.

### 2. The publish record (prose and data)

- Files: `publish.yaml`.
- No tests beyond R6: the record is listing text and data.

1. **`description`:**
    - which tool: the Commercial Electric wire stripper and crimper, with one curved and one straight steel handle;
    - which grip is which;
    - the fit: snug in TPU 95A, holds without glue. The grooves inside give glue something to key into if wanted, and survive vapor-smoothing;
    - the flared open end;
    - the fit tests: print one first to check the bore near the open end.
2. **`manufacturing`:** TPU 95A; open end down; no supports. No slicer coaching (operator norm).
3. **`tags`:** 10 to 20 specific tags (Cults advice).
4. **`license_code`:** `gpl`, as every model in the catalog.
5. **`category_id` and `subcategory_ids`:** Tool, with Hand Tools and Spare Parts.
6. **`files`:** both grips and both fit tests, STL and STEP each, as the other models ship STL and STEP.
7. **`cults_creation_id`:** stays empty until the first publish. `name` stays. The photos (`img/`) are the operator's.

### 3. Publishing clean-up of the model directory (prose/policy)

- Files:
    - `README.md`;
    - `memory-bank/productContext.md`, `systemPatterns.md`, `techContext.md`;
    - the docstrings and comments in `grips.py` and `steel.py`.
- No tests: prose/policy artifact. A docstring or comment change is followed by a rebuild, and R1 must stay green.

1. Describe the two grips that ship and why they are shaped so. Remove:
    - the iteration-by-iteration history (the flare's prints, the closed end's history);
    - commit hashes;
    - "test print", "in progress" and "later task" wording that no longer holds.
2. **Keep:**
    - the reasoning (why the flare, why the bevel, why each closed end, the shut gap and its provenance);
    - the dated measurement log as a log.
3. **`systemPatterns.md` "Test prints":** describe the fit tests for users. The "record each test print as a SumMem note" rule stays as a contributor norm.
4. **SumMem:** record the decision and where the alternatives live: the full-length straight grip `3046d4e`, the shorter curved grip `a61aa6d`.
5. **Commit** the record and the clean-up together: `chore: saving progress on wire-stripper-grips-closed-end`.

### 4. Final verification (executable)

1. Rerun every check on the committed files, and the catalog suite.
2. Confirm the working tree is clean.

## Technology Validation

No new technology - validation not required.

## Dependencies

- The baselines in `.scratch/wirestripper-grip/baseline/`: `*-iter5.stl` and `*-5d73490.step` (curved, equal to `e1b3528`), and `*-iter2.stl` and `*-a61aa6d.step` (straight).
- The Cults category ids (read from the API on 2026-11-02).

## Challenges & Mitigations

- **The curved STL is not byte-identical** after the branch is added.
    - Mitigation: keep `5d73490`'s code verbatim in the length branch (same expressions, same order), including `ribs()`' positions.
    - If bytes still differ, compare CAD sections against `curved_grip-5d73490.step` (`slice_compare.py`, all heights including the closed end). Report it: a difference under 1e-6 is float noise, not a design change.
- **Two closed ends in one source read as clutter.** One dict and one branch, with the reason in a comment: the test prints chose them. No third style, and no shared abstraction for two cases.
- **The tool's exact model is unknown.** The description names the tool by brand and the handle shapes. The report asks the operator for a model or SKU to add.

## Pre-Mortem

- **The operator meant "keep the files", not "rebuild from source".** Byte-identical outputs satisfy both.
- **The clean-up drops something a later contributor needs.** The reasons stay; only the narrative and the hashes go. The alternatives' commits go to SumMem, and the measurement log stays whole.
- **The listing text over-promises.** It says only what the prints showed: both grips fit and hold dry. Whether glue was tested is not claimed.

## Build Progress

- [x] 1. The pair from one source.
    - `END_CLEAR = {"curved": 1.0, "straight": None}`.
    - `gap_roof()` is `5d73490`'s `roof()` verbatim. `tip_roof()` is the renamed roof. `closed_end()` returns `(past, ridge)`.
    - `bore()` and `ribs()` branch, each keeping its own iteration's code. The rib rule must differ per closed end: the straight grip's last rib section is 4.299999999999997, not 4.3, so a shared `s >= s_full` rule would have changed its STL.
    - Guard: `END_CLEAR` is `None` or above 0. `tip_roof` runs only for `None`.
    - `sizes()`: the last row and the closed-end line per grip.
    - Red first:
        - `pair_check.py`: 8 curved failures;
        - `design_guards.py`: no `END_CLEAR` guard, and no `KeyError`;
        - `report_check.py`: the curved grip's rows;
        - `closed_end.py`: no `closed_end`.
    - Green:
        - `pair_check.py`: built and committed, all four STLs byte for byte, and the STEP files past `FILE_NAME`. The curved files equal `e1b3528`'s, and the straight files `a61aa6d`'s. The STEP files were restored from git (preflight A1).
        - R2, R3 and R5 pass.
        - R4 (`verify.py`): the curved grip's bite is −0.52% against 8 ribs over L, and its cap is 5.000. The straight grip's checks are as before.
        - `tools/overhang.py` flags only the ridge strips.
- [ ] 2. The publish record.
- [ ] 3. Publishing clean-up.
- [ ] 4. Final verification.

## Status

- [x] Initialization complete
- [x] Test planning complete (TDD)
- [x] Implementation plan complete
- [x] Technology validation complete
- [x] Pre-Mortem complete
- [ ] Preflight
- [ ] Build
- [ ] QA
