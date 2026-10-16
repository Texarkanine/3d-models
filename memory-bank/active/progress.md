# Progress

**Complexity:** Level 1

Cults returns unpadded global ids. `creationsBatch` filters by slug decoded from that id; strict base64 decode failed and fell back to the opaque string, so updates failed after the first create.
