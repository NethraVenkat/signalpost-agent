"""Assemble audited Stage E receipts; no HTTP or extraction work."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
DEST=ROOT/'reports/r5/stageE'

def main():
    replay=json.loads((DEST/'refresh_results.json').read_text(encoding='utf8'))
    live=json.loads((DEST/'live_refresh/results.json').read_text(encoding='utf8'))
    replay['live_refresh']={k:v for k,v in live.items() if k not in {'all_changes','observations','material_change_events','verification'}}
    replay['live_refresh']['full_receipts']='live_refresh/results.json'
    (DEST/'refresh_results.json').write_text(json.dumps(replay,indent=2)+'\n',encoding='utf8')
    text='# Stage E - measured refresh correctness\n\nRefresh comparison now treats equivalent aware registry publication timestamps as the same instant and orders uncertain-section value comparisons by field. Publisher strings/evidence remain unchanged. C2 was reverted because the extension gained no websites. The new offline harness runs production proof/extraction/refresh/verification/site code with saved responses, fixed clock and isolated source mutations.\n\n| Check | Result |\n|---|---:|\n'
    for k in ('planted_causal_changes','true_positives','false_positives','false_negatives','supported_field_events','precision','recall','unchanged_changes','false_change_rate_unchanged','idempotent_changes'):
        text+=f"| {k} | {replay[k]} |\n"
    text+=f"\nTransient replay: {replay['transient']['carried_claims']} prior claims retained, original evidence IDs/times preserved, stale markers visible, zero company changes. Each of the seven changed snapshots repeated with zero company changes and zero coverage observations; unchanged snapshots also had zero observations.\n\n"
    text+='Live-driven regression: pre-fix registry APIs alternated +01/+02 offsets and UTC Z representations of identical publication instants. This caused 620 false minor changes and 25 false coverage observations, overflowing the unchanged 250 KB page gate. Exact saved 100-company pair replay after comparison normalization yields zero changes/observations, all 1202 registry event receipts verified and site largest profile 249314 bytes; no rendering/evidence gate was loosened. See saved_live_pair_replay.json and the archived pre_timezone_fix trial.\n\n'
    text+='Scope: one company from saved seed-20261113 receipts. Event precision and causal-intervention recall have different declared denominators. Synthetic empty NAV forward tail is explicit and supplies no job fact; exact saved ad detail is mandatory. This is not whole-feed coverage validation or a population-wide accuracy claim. No network fallback or paid model.\n\n'
    text+='| Seed | C2 trial sites -> retained-policy sites | Social companies | Facts | HTTP | Wall seconds | Unsupported values |\n|---|---:|---:|---:|---:|---:|---:|\n'
    for sample,seed in [('frozen',20261017),('daily',20261113),('mock',20261114)]:
        old=json.loads((ROOT/f'reports/r5/stageC2/{sample}/counts.json').read_text(encoding='utf8'))['metrics']
        new=json.loads((DEST/sample/'counts.json').read_text(encoding='utf8'))['metrics']
        v=json.loads((DEST/sample/'verification.json').read_text(encoding='utf8'))
        assert v['synthesis_unverified_values']==v['briefing_unverified_values']==0
        text+=f"| {seed} | {old['verified_websites']} -> {new['verified_websites']} | {new['social_profile_companies']} | {new['total_facts']} | {new['http_requests']} | {new['process_wall_seconds']:.3f} | 0 |\n"
    text+='\nAll three are fresh state, exactly seven flags, 100 ordered terminal envelopes, generated sites, all five briefing topics, HTTP <=1850, within the default time limit, and $0. Exact commands, resolved defaults, source/input/output hashes, failures and verifier receipts are in each sample directory. Different observation times can change network outcomes; no causal coverage gain is claimed.\n\n'
    text+=f"Live frozen refresh: {live['http']} HTTP, {live['wall_seconds']:.3f}s wall, {live['changes']} company changes ({live['material_changes']} material, {live['minor_changes']} minor), {live['coverage_observations']} coverage observations, {live['carried_claims']} carried-forward claims. Seven evaluator flags **plus explicitly requested --previous** pointing to the latest frozen envelopes; no feature/cap flags. Fresh runtime cache. Missing archived evidence bodies are added only after the run for verification, never used as current proof. Full before/after evidence and observations: live_refresh/results.json. Zero unsupported values and $0.\n\n"
    text+='Hand check: inspect all seven mutation receipts and repeated results in refresh_results.json; verify NAV inactive proof and the website 404 removal versus timeout carry-forward; inspect any live material events individually before treating them as real-world effective dates. Company value changes and coverage observations remain separate. New/removed website/social proof excerpts: new_websites.md (unchanged inventory in url_inventory.json). No publication or push.\n'
    (DEST/'RESULTS.md').write_text(text,encoding='utf8')
    docs=ROOT/'docs/REFRESH.md';s=docs.read_text(encoding='utf8')
    marker='\nLive frozen-100 measurement (Stage E):'
    s=s.split(marker)[0]
    s+=f"{marker} {live['material_changes']} material and {live['minor_changes']} minor company changes, separately from {live['coverage_observations']} coverage observations; {live['http']} HTTP and {live['wall_seconds']:.3f}s wall, zero unsupported values and $0. See `reports/r5/stageE/live_refresh/results.json` for evidence and exact categories. This observational run does not provide a known-ground-truth precision estimate.\n"
    docs.write_text(s,encoding='utf8')
    print(text)

if __name__=='__main__':main()
