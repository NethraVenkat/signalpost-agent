import json
import pytest
from scripts.verify_output import verify
from tests.test_registry import config, execute


@pytest.mark.parametrize('shape', ['union','contract','reference'])
def test_verifier_receives_observation_date_for_recent_registry_events(tmp_path, shape):
    from signalpost.models.envelope import Envelope
    from signalpost.models.shapes import serialize
    from signalpost.synthesis.template import generate
    from scripts.verify_output import verify_synthesis
    cfg=config(tmp_path,['923609016'])
    _,rows=execute(cfg)
    row=Envelope.model_validate(rows[0])
    registration=next(c for c in row.claims if c.field=='identity.registration_date' and c.availability=='available')
    row.run.completed_at=registration.value[:10]+'T00:00:00Z'
    row.completed_at=row.run.completed_at
    row.run.synthesis=generate(row);row.profile.synthesis=row.run.synthesis
    assert any(s.text.startswith('Registered in Enhetsregisteret:') for s in row.run.synthesis.sections.changes)
    assert verify_synthesis(serialize(row,shape))[0]==1


def test_verification_rejects_missing_membership_and_corrupt_sources(tmp_path):
    cfg = config(tmp_path, ['923609016'])
    execute(cfg)
    verify(cfg.output, cfg.state_dir, 1, cfg.organisations, cfg.report, True)
    with pytest.raises(AssertionError):
        verify(cfg.output, cfg.state_dir, 2)
    row = json.loads(cfg.output.read_text().splitlines()[0])
    sha = next(e['content_sha256'] for e in row['evidence'])
    (cfg.state_dir / 'blobs' / sha).write_bytes(b'corrupted')
    with pytest.raises(AssertionError):
        verify(cfg.output, cfg.state_dir, 1)
