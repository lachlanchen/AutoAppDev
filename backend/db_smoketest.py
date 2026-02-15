import asyncio
import os
import sys
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

import asyncpg
from dotenv import load_dotenv


REPO_ROOT = Path(__file__).resolve().parents[1]


def _load_env() -> None:
    load_dotenv(dotenv_path=REPO_ROOT / ".env", override=False)


def _sanitize_dsn(dsn: str) -> str:
    dsn = (dsn or "").strip()
    if "://" in dsn:
        try:
            parts = urlsplit(dsn)
            if parts.password is None:
                return dsn
            user = parts.username or ""
            host = parts.hostname or ""
            port = f":{parts.port}" if parts.port else ""
            netloc = f"{user}:***@{host}{port}" if user else f"***@{host}{port}"
            return urlunsplit((parts.scheme, netloc, parts.path, parts.query, parts.fragment))
        except Exception:
            return dsn

    # Best-effort for non-URL DSNs.
    lowered = dsn.lower()
    if "password=" in lowered:
        out = []
        for token in dsn.split():
            if token.lower().startswith("password="):
                out.append("password=***")
            else:
                out.append(token)
        return " ".join(out)

    return dsn


async def _run() -> int:
    _load_env()

    dsn = os.getenv("DATABASE_URL", "").strip()
    if not dsn:
        print("ERROR: missing required env: DATABASE_URL", file=sys.stderr)
        print("Hint: cp .env.example .env and set DATABASE_URL (see docs/env.md).", file=sys.stderr)
        return 2

    conn = None
    try:
        # Use asyncpg's built-in timeout to avoid hangs during DNS/connection setup.
        conn = await asyncpg.connect(dsn=dsn, timeout=2.0)
        v = await conn.fetchval("SELECT 1", timeout=2.0)
        if int(v) != 1:
            print(f"ERROR: unexpected SELECT 1 result: {v!r}", file=sys.stderr)
            return 3
        print("OK: postgres SELECT 1")
        return 0
    except asyncio.TimeoutError:
        print("ERROR: postgres connection/query timed out (2s)", file=sys.stderr)
        print(f"DSN: {_sanitize_dsn(dsn)}", file=sys.stderr)
        return 4
    except TimeoutError:
        print("ERROR: postgres connection/query timed out (2s)", file=sys.stderr)
        print(f"DSN: {_sanitize_dsn(dsn)}", file=sys.stderr)
        return 4
    except Exception as e:
        print(f"ERROR: postgres smoke test failed: {type(e).__name__}: {e}", file=sys.stderr)
        print(f"DSN: {_sanitize_dsn(dsn)}", file=sys.stderr)
        print("Hint: verify Postgres is running and DATABASE_URL is correct (see docs/env.md).", file=sys.stderr)
        return 5
    finally:
        if conn is not None:
            try:
                await conn.close()
            except Exception:
                pass


def main() -> None:
    # Avoid asyncio.run() to prevent shutdown waits on lingering resolver threads.
    # This is a smoke-test CLI, so a hard exit is acceptable and keeps it deterministic.
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        rc = loop.run_until_complete(_run())
    finally:
        try:
            loop.stop()
            loop.close()
        except Exception:
            pass
    try:
        sys.stdout.flush()
        sys.stderr.flush()
    finally:
        os._exit(int(rc))


if __name__ == "__main__":
    main()
