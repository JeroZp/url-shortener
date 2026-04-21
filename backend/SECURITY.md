# Security Notes

## Ignored Vulnerabilities

### GHSA-7f5h-v6xp-fcq8 (starlette)

**Affected package:** starlette (transitive dependency of FastAPI)
**Severity:** Medium (DoS via multipart form parsing)
**Status:** Ignored — not applicable to this application

**Justification:**
This vulnerability affects applications that parse multipart/form-data requests.
Our URL shortener API only accepts JSON payloads (Content-Type: application/json).
We do not use any FastAPI endpoints with `Form()` or `File()` parameters.

The fix (starlette 0.49.1) is not yet compatible with our FastAPI version,
and pinning it would break the dependency resolution. When FastAPI releases
a version compatible with starlette 0.49+, this ignore rule will be removed.
