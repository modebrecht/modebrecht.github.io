#!/usr/bin/env python3
"""BO2026 Windows Emergency Recovery.

This is the human-readable source used to build BO2026-Recovery-Windows.exe.
The shared browser-recovery core is embedded in ../bo2026-recovery.html and is
bundled into the executable by PyInstaller. Keeping the core in one place
prevents the web/macOS and Windows recovery implementations from drifting.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import urlsplit

TARGET_MARKER = 'HOST="bo2026.vercel.app"; ORIGIN="https://bo2026.vercel.app"; KIND="cv-cover-charm-dossier"; VERSION=1'
OUT_MARKER = 'OUT=DESKTOP/f"BO2026-Recovery-{STAMP}"'
TARGETS = {
    "1": ("Vercel", "bo2026.vercel.app", "https://bo2026.vercel.app"),
    "2": ("Render", "dev-bo2026.onrender.com", "https://dev-bo2026.onrender.com"),
}


def bundled_path(name: str) -> Path:
    """Return a path both from source checkout and from a PyInstaller bundle."""
    bundle_root = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent.parent))
    candidate = bundle_root / name
    if candidate.exists():
        return candidate

    # Source-tree fallback when running recovery/bo2026_recover_windows.py directly.
    candidate = Path(__file__).resolve().parent.parent / name
    if candidate.exists():
        return candidate
    raise FileNotFoundError(f"Bundled recovery resource not found: {name}")


def load_base_source() -> str:
    html = bundled_path("bo2026-recovery.html").read_text(encoding="utf-8")
    match = re.search(
        r'<script type="text/plain" id="recoveryPython">(.*?)</script>',
        html,
        flags=re.S,
    )
    if not match:
        raise RuntimeError("Embedded recoveryPython script not found")
    source = match.group(1).lstrip()
    if TARGET_MARKER not in source:
        raise RuntimeError("Recovery target marker not found")
    if OUT_MARKER not in source:
        raise RuntimeError("Recovery output marker not found")
    return source


def normalize_custom(raw: str) -> tuple[str, str, str]:
    """Normalize a user-entered domain/URL to (label, host, origin)."""
    value = (raw or "").strip()
    if not value:
        raise ValueError("Keine Domain eingegeben.")
    if "://" not in value:
        value = "https://" + value

    parsed = urlsplit(value)
    scheme = parsed.scheme.lower()
    if scheme not in {"http", "https"}:
        raise ValueError("Nur http:// oder https:// werden unterstützt.")
    if not parsed.hostname:
        raise ValueError("Keine gültige Domain erkannt.")
    if parsed.username or parsed.password:
        raise ValueError("Benutzername/Passwort in der URL werden nicht unterstützt.")

    try:
        port = parsed.port
    except ValueError as exc:
        raise ValueError("Ungültiger Port.") from exc

    hostname = parsed.hostname.lower()
    netloc = f"[{hostname}]" if ":" in hostname and not hostname.startswith("[") else hostname
    if port is not None:
        netloc += f":{port}"

    origin = f"{scheme}://{netloc}"
    safe = "".join(c if c.isalnum() or c in "-_." else "_" for c in netloc)
    return (f"Custom-{safe}", netloc, origin)


def run_target(label: str, host: str, origin: str) -> None:
    print("\n" + "=" * 64)
    print(f"BO2026 Recovery: {label}")
    print(f"Quelle: {origin}")
    print("=" * 64)

    base_source = load_base_source()
    replacement = f'HOST="{host}"; ORIGIN="{origin}"; KIND="cv-cover-charm-dossier"; VERSION=1'
    source = base_source.replace(TARGET_MARKER, replacement, 1)
    source = source.replace(
        OUT_MARKER,
        f'OUT=DESKTOP/f"BO2026-Recovery-{label}-{{STAMP}}"',
        1,
    )

    namespace = {"__name__": f"bo2026_recovery_{label.lower()}"}
    exec(compile(source, f"<bo2026-recovery-{label.lower()}>", "exec"), namespace)
    namespace["main"]()


def choose_targets() -> list[tuple[str, str, str]]:
    while True:
        print("BO2026 Emergency Recovery")
        print("-------------------------")
        print("Welche Browserdaten sollen gerettet werden?")
        print("  1  Vercel  - bo2026.vercel.app")
        print("  2  Render  - dev-bo2026.onrender.com")
        print("  3  Beide durchsuchen")
        print("  4  Eigene Domain eingeben")
        print("\nEnter ohne Eingabe = Beide (empfohlen)")

        try:
            choice = input("Auswahl [3]: ").strip()
        except (EOFError, KeyboardInterrupt):
            choice = "3"

        if choice == "1":
            return [TARGETS["1"]]
        if choice == "2":
            return [TARGETS["2"]]
        if choice in {"", "3"}:
            return [TARGETS["1"], TARGETS["2"]]
        if choice == "4":
            try:
                raw = input("Domain/URL (z.B. bo.schule.ch): ").strip()
                target = normalize_custom(raw)
                print(f"Erkannte Origin: {target[2]}")
                return [target]
            except (EOFError, KeyboardInterrupt):
                return [TARGETS["1"], TARGETS["2"]]
            except ValueError as exc:
                print(f"Ungültige Domain: {exc}\n")
                continue

        print("Bitte 1, 2, 3 oder 4 eingeben.\n")


def main() -> None:
    selected = choose_targets()
    for target in selected:
        try:
            run_target(*target)
        except Exception as exc:
            print(f"\nFEHLER bei {target[0]}: {exc}")

    print("\n" + "=" * 64)
    print("Recovery abgeschlossen.")
    print("Pruefe auf dem Desktop die BO2026-Recovery-* Ordner.")
    print("=" * 64)
    if sys.stdin.isatty():
        try:
            input("Enter zum Schliessen ...")
        except (EOFError, KeyboardInterrupt):
            pass


if __name__ == "__main__":
    main()
