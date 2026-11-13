"""Prove the HIGH fixture fails with both retained buggy extractors."""
import hashlib
import importlib.util
import json
import sys
from audit import DEST, ROOT
sys.path.insert(0, str(ROOT))
from signalpost.web import publisher_veto
from tests import test_publisher_veto as fixture


def main():
    original_extract = publisher_veto.extract_publisher
    original_score = fixture.score
    captured = []
    def score(*args, **kwargs):
        result = original_score(*args, **kwargs)
        captured.append({'level': result.level, 'reason': result.reason, 'points': result.points})
        return result
    fixture.score = score
    cases = [('overbroad_header', DEST / 'trials/overbroad_header/publisher_before_header_fix.py'),
             ('short_contact_wrapper', DEST / 'trials/short_contact_wrapper/publisher_before_contact_fix.py'),
             ('copyright_wrapper', DEST / 'trials/copyright_wrapper/publisher_before_copyright_fix.py')]
    results = []
    try:
        for label, path in cases:
            spec = importlib.util.spec_from_file_location('stageW_regression_' + label, path)
            module = importlib.util.module_from_spec(spec); sys.modules[spec.name] = module; spec.loader.exec_module(module)
            publisher_veto.extract_publisher = module.extract_publisher
            failed = False
            try:
                fixture.test_biography_group_name_outside_real_header_does_not_veto()
            except AssertionError:
                failed = True
            assert failed and captured[-1]['level'] == 'REJECT'
            results.append({'extractor': label, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'test_failed_as_expected': failed, **captured[-1]})
        publisher_veto.extract_publisher = original_extract
        fixture.test_biography_group_name_outside_real_header_does_not_veto()
        assert captured[-1]['level'] == 'HIGH'
        results.append({'extractor': 'accepted', 'test_passed': True, **captured[-1]})
    finally:
        publisher_veto.extract_publisher = original_extract
        fixture.score = original_score
    output = {'method': 'One authored synthetic fixture, actual retained before-fix extractor code versus current extractor. No network, output editing, new proof tier or threshold change.',
              'fixture': 'tests/test_publisher_veto.py::test_biography_group_name_outside_real_header_does_not_veto', 'results': results}
    (DEST / 'r4_regression_before_after.json').write_text(json.dumps(output, indent=2) + '\n', encoding='utf8', newline='\n')
    print(json.dumps(output))


if __name__ == '__main__':
    main()
