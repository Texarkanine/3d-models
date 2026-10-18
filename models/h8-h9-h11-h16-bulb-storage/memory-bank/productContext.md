# Product Context

## Target Audience

- People who keep spare H11 headlamp or fog bulbs, halogen or LED, and own a home FDM 3D printer. H8, H9 and H16 bulbs use the same cap (PGJ19), so they are covered too.
- The operator first. They have halogen H11s (stamped steel fins, with a spring nub) and LED H11s (thicker cast fins, no nub). The design will be shared publicly, so it must fit any bulb that meets the cap standard.

## Use Cases

- Store a spare bulb in a glovebox, bag, bin or car without harming the glass or the LEDs.
- Put a bulb in and take it out by hand, many times, with the same push-and-twist as a headlamp socket.
- Fit a non-standard bulb by measuring it (`measure_cap.svg`) and changing a few dimensions before printing.
- Keep the pins in the bulb's connector clean in storage, with a separate cap that latches on like the car's plug.

## Key Benefits

- Twist-lock, like the car's socket: push the fins through the openings, twist, and it locks.
- Locks bulbs with or without the halogen spring nub.
- One holder fits H8, H9, H11 and H16. The bulb may sit loose until it is twisted.
- Prints without supports.

## Success Criteria

- Fits every bulb within cap PGJ19 (-1, -2, -3 and -5) at its largest sizes, plus clearance, and the operator's halogen and LED H11s; confirmed by test prints.
- An LED H11 without a spring nub stays locked in storage and comes out with a firm twist back.
- Prints in one obvious orientation with no supports. The face the fins press against is clean.
- Files open in a slicer (STL) and in Solid Edge Community Edition (STEP).
- The connector cap clicks onto any connector within the standard, stays on in a bag, and comes off with a squeeze and a pull.

## Key Constraints

- Build to the published standard plus clearance. The operator's bulbs are data points. LED retrofits are the reason this model exists, so where measured LED fins exceed the standard, the defaults widen to take them. A bulb that still does not fit is handled by changing dimensions.
- Faces that locate or hold the bulb must print without supports and without sagging. Cosmetic faces may take supports if they break off easily.
- Small enough to store compactly.
- Instructions are for home-printer users: plain language, no trade jargon.
- Everything in the repository may become public, so it must be shareable.
