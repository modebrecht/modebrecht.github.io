# BO2026 Recovery source

This folder contains the human-readable source for the Windows emergency recovery tool.

## Files

- `bo2026_recover_windows.py` — source for `BO2026-Recovery-Windows.exe`.
- `../bo2026-recovery.html` — the shared recovery core and web recovery UI. The Python core inside this HTML file is bundled into the Windows EXE during the build so the browser-recovery logic has one source of truth.
- `../.github/workflows/build-bo2026-recovery.yml` — validates the source, builds the standalone Windows EXE with PyInstaller, smoke-tests it, creates a SHA-256 checksum, and publishes the stable GitHub Release assets.

## Windows EXE choices

At startup the executable can recover data for:

1. `https://bo2026.vercel.app`
2. `https://dev-bo2026.onrender.com`
3. both origins
4. a custom `http://` or `https://` origin entered by the user

Custom URLs are normalized to their browser origin (`scheme + host + optional port`). Paths, query strings and fragments do not affect `localStorage` origin selection.

## Build

The canonical build runs in GitHub Actions. PyInstaller bundles `bo2026-recovery.html` into the one-file executable, so the released EXE does not need an external HTML file at runtime.

The release also contains a `.sha256` file for integrity verification.
