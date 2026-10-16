# Progress

After an update deploy removes old Cults photos and files, bump the creation so the public gallery rebuilds from the tag's final images and STL previews.

**Complexity:** Level 1

## 2026-10-15 - COMPLEXITY-ANALYSIS - COMPLETE

* Work completed
    - Confirmed the task is [issue 4](https://github.com/Texarkanine/3d-models/issues/4)
    - Classified the work
* Decisions made
    - Level 1: the failure is in one publisher path, and the fix is a field change after the old assets are removed
* Insights
    - Cults rebuilds the page gallery only when `updatedAt` changes, and asset add or delete does not change it

## 2026-10-15 - BUILD - COMPLETE

* Work completed
    - After the old assets are removed, the publisher changes `details` and restores it
    - It waits until every STL from the tag has a preview image before that change
    - 66 catalog tests passed
* Decisions made
    - `details` is the field that gets edited, because that edit rebuilt the gallery on the live listing
    - `updateIllustration` is not used: its only argument is position
    - STEP files do not hold up the edit; the page shows one preview per STL
    - The optional asset read-back is not part of this fix
* Insights
    - A gallery built before an STL preview exists keeps missing that preview
    - A free details edit still has to send `downloadPrice` 0 and `licenseCode`
