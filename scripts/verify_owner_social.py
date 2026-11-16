"""Replay owner social declarations against original pages and official identity."""
from signalpost.web.html import Page
from signalpost.web.policy import domain
from signalpost.web.owner_social import declared_profiles
from scripts.verify_publisher_identity import registry_context

TIERS={'owner_jsonld_sameas_v1','own_contact_follow_us_v1'}

def verify(org,data,evidence,stored_body):
    total=0
    for claim in data['claims']:
        if not claim['field'].startswith('social_profile.') or claim['availability']!='available':continue
        value=claim['value']
        if value.get('proof_tier') not in TIERS:continue
        site=next((c for c in data['claims'] if c['field']=='official_website' and c['availability']=='available'),None)
        assert site and site['value']['identity_level'] in {'HIGH','VERIFIED'},'Owner social requires a verified/HIGH website'
        assert not site['value'].get('other_orgnrs') and site['value'].get('relationship_note')!='group_site','Group social declaration'
        context,refs=registry_context(org,data,evidence,stored_body)
        name_refs={r for c in data['claims'] if c['field']=='identity.legal_name' and c['availability']=='available' for r in c['evidence_ids']}
        assert name_refs and name_refs<=set(claim['evidence_ids']),'Missing legal-name dependencies'
        assert set(site['evidence_ids'])<=set(claim['evidence_ids']),'Missing verified-site dependencies'
        assert value['company_name']==context['name'],'Unsupported social legal name'
        receipt=value.get('owner_declaration');matched=False
        for ref in claim['evidence_ids']:
            e=evidence[ref]
            if e['source_class']!='company_owned' or e['locator']!='company-link:'+value['url']:continue
            assert domain(e['source_url'])==domain(site['value']['final_url']),'Foreign social publisher'
            text=stored_body(e['content_sha256'])
            page=Page(text.encode('utf8'),e['source_url'],text=text)
            expected=declared_profiles(page,context['name'],org,context).get(value['url'])
            matched |= bool(expected and expected==receipt and expected['tier']==value['proof_tier'] and expected['span']==e['claim_span'])
        assert matched,'Unsupported owner social declaration'
        total+=1
    return total
