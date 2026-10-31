# Decision: Bore fit and glue key

## Context

**What:** How the inside of the TPU 95A curved grip touches the steel. That covers what holds it on, what makes room for glue, and how it slides on.

**Why it matters:** This sets the shape of the bore, which is the one part of the grip that must match the measured steel. Get it wrong and the grip won't go on, falls off, or leaves glue nowhere to go. The fit-test print and every later test print depend on it.

**Constraints:**
- It slides on by hand and stays on without glue in normal use. The operator thinks TPU alone may be enough.
- Glue is optional and needs a designed surface that is still there after vapor smoothing, which removes print lines inside as well as outside.
- TPU 95A is stiff to stretch over a part: the jerry can buffer lists TPU 95 as hard to attach.
- The readings vary. The two passes at S1 to S3 differ by up to 0.34 mm in W, and printed TPU holes come out a tenth or two off.
- The steel tapers strongly in W (0.03 to 0.05 mm per mm) and barely in T (0.001 to 0.006 mm per mm).
- The steel's corner radii are not measured. The channel holds a ribbed plastic insert on one face, which may not be flush with the steel edges.
- The 3 mm holes D1 and D2 are centred on the faces seen with the tool lying flat.
- It prints open end down, standing up and leaning up to about 15 degrees, without support.
- The fit must be quick to tune: the fit-test print changes a parameter or two, not the design.

## Options Evaluated

- **A. Plain interference bore:** the bore is the steel's outline shrunk evenly on every face. Separate shallow grooves hold glue.
- **B. Longitudinal crush ribs:** the bore is the steel plus clearance. Small ribs along the length press into the steel by a set amount. The valleys between the ribs are the glue channels.
- **C. Circumferential lands and grooves:** rings around the bore alternate a tight land with a glue groove.
- **D. Clearance bore, glued on:** a loose bore that relies on glue.

## Analysis

| Criterion | A. Plain interference | B. Crush ribs | C. Rings | D. Clearance + glue |
|---|---|---|---|---|
| Stays on without glue | Yes | Yes | Yes | **No**, which fails the constraint |
| Slide-on force in TPU 95A | High: whole walls stretch, and T rubs the full 83 mm | Low: only rib tips deform | High: every land stretches the whole ring | None |
| Tolerance to ±0.35 reading spread and print error | Poor: the force swings widely | Good: small ribs absorb it | Poor | Good |
| Glue surface after smoothing | Only from the added grooves | Built in: 0.3 mm valleys along the full length | Built in | Built in |
| Glue and air escape while sliding on | Poor | Good: the valleys vent along the length | Poor: each ring traps glue | Good |
| Prints standing up | Fine | Fine: ribs are vertical walls | Each groove roof is an overhang, tilted up to 15 degrees by the curve | Fine |
| Insert or corner unknowns | Corners bind | Corners clear, ribs sit on firm steel near the corners | Corners bind | Not affected |
| Tuning after a fit test | One number, but sensitive | Two numbers (clearance, rib reach), forgiving | Several | Not applicable |

Key insights:
- **The W taper does the sliding work.** While the grip is still d mm short of seated, each part of the bore sits over steel that is narrower by about 0.03 to 0.05 × d. In W, the ribs only bite in the last few millimetres. T barely tapers, so T contact rubs along the whole length. T contact should therefore be lighter than W contact, and the friction that holds the grip comes mostly from W near the open end.
- **The old grip did the opposite.** It was loose in W (10.0 against about 9.6) and tight in T (14.14 against about 14.31), and it was glued. Copying its fit is not a goal.
- **Ribs near the corners solve two unknowns at once.** They stay clear of the holes, which are centred on their faces. They also bear on solid steel near the edges, not on the insert, whose height relative to the steel is unknown.
- **Glue channels must vent.** A grip pushed on over wet glue needs a path for glue and air along its length. Only lengthwise features give one.

## Decision

**Selected:** B. Longitudinal crush ribs.

**Rationale:** It is the only option that meets all three constraints at once: it holds without glue, slides on by hand in TPU 95A, and keeps a glue surface that survives smoothing. It absorbs the reading spread and print error. Its ribs print as vertical walls, and it gives the fit test one or two clear numbers to tune. Crush ribs are the standard way to press-fit plastic onto a part with loose tolerances.

**Tradeoff:** Contact is on a few narrow ribs, not the whole face, so holding force depends on how the ribs print. The fit test is there to check that. The bore is more geometry to build than a plain shrunk outline.

## Implementation Notes

- **Bore outline:** the steel's W(s) × T(s) rectangle plus a clearance `BORE_CLEAR` on each side (starting value 0.3), following the centre line.
- **Corners:** the bore's corners stay tight, so even a sharp steel corner clears them. A rounded bore corner of radius r leaves r − √2(r − c) at the diagonal, where c is the clearance. Keep the radius at most 0.5 with c = 0.3, which leaves at least 0.2, and assert at least 0.15. Correction, 2026-10-31: an earlier note said to round the corners large. That pushes the bore into the steel's corner instead of clearing it.
- **Ribs:** two on each of the four faces, each sitting `RIB_INSET` from its corner (start at 1.5, so a rib bears on the flat even if the steel's bend radius is about 1). On the faces with holes, they stay clear of a 3 mm hole on the centre line, even at W ≈ 6.3 near A.
- **Rib profile:** a trapezoid, about 1.2 mm at the base and 0.5 mm at the tip.
- **Rib reach:** the ribs reach past the steel face by an interference set separately for each direction. Start with `RIB_BITE_W` 0.3 and `RIB_BITE_T` 0.15 per side; T is lighter because it rubs the whole length.
- **Rib ends:** the ribs run from the open end to just short of the bore's closed end, and are cut square there.
- **Tuning:** the fit-test print (a short piece of the open end) calibrates `BORE_CLEAR` and the bites. Those values and the reason for any change live in the source's comments.
- **Listing:** suggest a little soapy water or isopropyl alcohol to slide the grip on dry. Glue is optional.
- **Rejected for now:** a snap nub into D1. It is not needed while friction holds. It stays the fallback if a test print creeps off.
