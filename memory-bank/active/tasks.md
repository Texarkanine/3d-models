# Current Task: Remove Cults user-agent tests

**Complexity:** Level 1

## Fix

`HttpTransportTests` asserted that the Cults request's `User-Agent` equals `Texarkanine GitHub CICD for Cults3D`, and that no header contains `Python-urllib`. Those assertions go red only when the string changes. They do not show that Cults or Cloudflare accepts the request.

Removed the class and the imports it used (`urllib.request`, `USER_AGENT`, `_http_transport`) from `tests/test_cults_publish.py`. `tools/cults_publish.py` still sends the header. No replacement test.

## Files

- `tests/test_cults_publish.py`

## QA Results

- **Status**: PASS
- **Findings**: `HttpTransportTests` and its unused imports were cleanly removed from `tests/test_cults_publish.py`. The publisher still sends `User-Agent: Texarkanine GitHub CICD for Cults3D`. All 36 unit tests pass. No semantic, architectural, or regression issues found.
