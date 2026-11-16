"""Official bulk download for the audit's complete NAV parent/universe join."""
from signalpost.portable_paths import portable, portable_text  # saved paths stay repo-relative
import hashlib
import json
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.robotparser import RobotFileParser
import httpx

ROOT = Path(__file__).resolve().parents[3]
DEST = ROOT / '.data/r5/stageW/underenheter.csv'
URL = 'https://data.brreg.no/enhetsregisteret/api/underenheter/lastned/csv'


def main():
    if DEST.exists():
        raise SystemExit('Existing snapshot retained; refusing repeat download')
    DEST.parent.mkdir(parents=True, exist_ok=True)
    records = []
    with httpx.Client(timeout=httpx.Timeout(45, connect=10), trust_env=False, follow_redirects=False, headers={'User-Agent': 'Signalpost/1.3.0 official bulk audit'}) as client:
        robots = client.get('https://data.brreg.no/robots.txt')
        records.append({'url': str(robots.url), 'status': robots.status_code, 'body': robots.text})
        if robots.status_code == 200:
            parser = RobotFileParser(); parser.parse(robots.text.splitlines())
            if not parser.can_fetch('Signalpost', URL):
                raise SystemExit('robots refuses bulk download')
        elif robots.status_code not in {404, 410}:
            raise SystemExit('robots unavailable; no bulk request')
        time.sleep(1)
        sha = hashlib.sha256(); count = 0
        with client.stream('GET', URL) as response:
            response.raise_for_status()
            with DEST.open('xb') as target:
                for chunk in response.iter_bytes():
                    count += len(chunk)
                    if count > 512 * 1024 * 1024:
                        raise SystemExit('512 MiB download ceiling reached; partial is not accepted')
                    sha.update(chunk); target.write(portable_text(chunk))
            records.append({'url': URL, 'status': response.status_code, 'sha256': sha.hexdigest(), 'bytes': count, 'headers': dict(response.headers)})
    out = {'retrieved_at': datetime.now(timezone.utc).isoformat(), 'path': str(DEST), 'http_requests': 2, 'cost_usd': 0,
           'attribution': 'Brønnøysundregistrene, Enhetsregisteret, NLOD 2.0', 'requests': records}
    (Path(__file__).parent / 'subunit_snapshot.json').write_text(portable_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n'), encoding='utf8', newline='\n')
    print(json.dumps({'bytes': count, 'sha256': sha.hexdigest()}))


if __name__ == '__main__':
    main()
