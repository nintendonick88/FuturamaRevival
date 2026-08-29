# Original-client HTTP/HTTPS probe

This directory contains a deliberately disposable archaeology tool. It is not
the replacement server and does not establish the project's future
architecture.

`probe_server.py` accepts HTTP or HTTPS requests, records the method, path, headers and
body as JSON Lines, and returns a controlled response. Its purpose is to answer
small questions about the unmodified client with captured evidence.

Example:

```powershell
python probe_server.py `
  --cert D:\Android\experiment\server.crt `
  --key D:\Android\experiment\server.key `
  --log D:\Android\evidence\client-requests.jsonl
```

For a test APK whose service URL has been redirected to plain HTTP, omit
`--cert` and `--key`:

```powershell
python probe_server.py --host 0.0.0.0 --port 8302 `
  --log D:\Android\evidence\client-requests.jsonl
```

The default response is HTTP 503 with an
`X-Futurama-Preservation-Probe: 1` header. A specific response body and status
can be supplied with `--response-file` and `--status` only after capture data
supports that experiment.

`--gzip-response` and repeatable `--response-header NAME:VALUE` options allow a
captured response's transport details to be reproduced independently of its
body. They are controlled experiment variables, not claims that a header is
required.

## Test APK URL patch

`patch_service_url.py` creates a separate APK and changes only the exact native
service URL. It requires the replacement to be no longer than the original and
preserves the native library's byte length. The resulting APK still needs to be
zip-aligned and signed with a local Android test key before installation.
