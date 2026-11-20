import hashlib
from pathlib import Path
from types import SimpleNamespace

import pytest
from signalpost.web.candidates import Candidate
from signalpost.web.collector import candidate_proof
from signalpost.web.html import Page
from signalpost.web.publisher_identity import declared_receipt, name_fragment, DECLARED

ORG = '923609016'
FILL = 'Ordinary information about business services. ' * 12


@pytest.mark.parametrize(('org', 'digest', 'publisher', 'context', 'tier'), [
    ('989087126', '1f664cdb8c82a8e231b8ed1f941e14d802a621426a82db6d917ab7012a2e022c',
     '<title>Forside - Areto Revisjon AS Statsautorisert Revisor</title>\n'
     '<span class="elementor-icon-list-text">post@aretorevisjon.no</span>',
     {'name': 'ARETO REVISJON AS', 'website': 'www.aretorevisjon.no', 'email': 'post@aretorevisjon.no',
      'street': 'Gravdalsveien 4', 'postcode': '5165', 'city': 'Laksevåg'}, DECLARED),
    ('975978729', '38bb4139565f130ad1f19909dcf7512f17619ac992d45935048859e946192643',
     '<title>Kistefos møbler - Kjøkken og kvalitetsmøbler - Kistefos Møbler</title>\n'
     '<link rel="canonical" href="https://kistefosmobler.no/" />',
     {'name': 'KISTEFOS MØBLER AS', 'website': 'www.kistefosmobler.no', 'email': 'post@kistefosmobler.no',
      'street': 'Rosteinvegen 6', 'postcode': '2870', 'city': 'Dokka', 'phone': '61 11 29 30'},
     'registry_declared_live'),
])
def test_saved_legacy_sites_publish_reconstructible_owner_receipts(org, digest, publisher, context, tier):
    from signalpost.runner import placeholder
    from signalpost.sources.extract import Section
    from signalpost.sources.http import Response
    from signalpost.web.collector import publish_result
    from signalpost.web.policy import domain, normalize_url

    archived = Path(__file__).resolve().parents[1] / 'out/r5-gap-trial-live/state/blobs' / digest
    if archived.is_file():
        body = archived.read_bytes()
        assert hashlib.sha256(body).hexdigest() == digest
        assert all(line.encode() in body for line in publisher.splitlines())
    else:
        # Recreate only the public receipt excerpts for a clean checkout.
        body = f'<html>{publisher}<main>{FILL}</main></html>'.encode()
    nominated = normalize_url(context['website'])
    url = nominated if org == '989087126' else 'https://kistefosmobler.no/'
    original = Page(body, url)
    candidate = Candidate(nominated, domain(nominated), 'registry_website')
    proof = candidate_proof(original, org, context, candidate, [])
    assert proof.level == 'HIGH' and proof.proof_type == tier

    now = '2026-11-20T00:00:00Z'
    response = Response(body, 200, url, now, hashlib.sha256(body).hexdigest())
    envelope = placeholder(org, 'publisher-receipt', now, ('website',))
    http = SimpleNamespace(accepted_pages={}, attempts={})
    section = publish_result(org, envelope, http, Section(),
                             [(candidate, proof, response, original, [(response, original)])], [], context)
    website = next(c for c in section.claims if c.field == 'official_website')
    assert website.value['publisher_identity']['proof_page_url'] == url
    assert website.value['final_url'] == url.rstrip('/')
    if org == '989087126':
        contact = next(c for c in section.claims if c.field.startswith('contact.email.'))
        assert contact.value == context['email']
        evidence = next(e for e in section.evidence if e.id in contact.evidence_ids)
        assert contact.value in evidence.claim_span and evidence.claim_span in original.raw


def page(markup, url='https://example.no/'):
    return Page(f'<html><main>{FILL}</main>{markup}</html>'.encode(),url)


def prove(markup, **context):
    return candidate_proof(page(markup), ORG, {'name':'Example AS','website':'www.example.no',**context},
                           Candidate('https://example.no/','example.no','registry_website'), [])


@pytest.mark.parametrize('markup', ['<title>Example AS</title>', '<meta property="og:site_name" content="Example AS">',
                                  '<header>Example AS</header>', '<footer>Example AS</footer>',
                                  '<div class="copyright">© Example AS</div>', '<address>Example AS; Telefon 12345678</address>'])
def test_declared_full_publisher_name_suffices_without_contact(markup):
    p=prove(markup)
    assert p.level=='HIGH' and p.proof_type==DECLARED and p.publisher_receipt['publisher_location']


@pytest.mark.parametrize('markup', ['<p>Example AS</p>', '<article><header>Example AS</header></article>',
                                  '<section class="clients"><h2>Example AS</h2></section>',
                                  '<footer>Levert av Example AS</footer>', '<footer>Example</footer>',
                                  '<footer>Example ASA</footer>', '<footer>Example-AS</footer>',
                                  '<footer hidden>Example AS</footer>'])
def test_body_suffixless_fuzzy_hidden_and_agency_names_do_not_qualify(markup):
    assert prove(markup).proof_type!=DECLARED


@pytest.mark.parametrize('credit',[
    'Utviklet av <a>Example AS</a>',
    '<span>Utviklet av</span><a>Example AS</a>',
    '<span>Utviklet</span><span>av</span><a>Example AS</a>',
    '<div>Design by <a><span class="copyright">© Example AS</span></a></div>',
    '<span>Levert av</span><a><img class="logo" alt="Example AS"></a>',
    '<p>Website by <span>Example AS</span></p>',
])
def test_split_agency_credit_never_becomes_publisher_identity(credit):
    assert prove('<title>Client AS</title><footer>© Client AS '+credit+'</footer>').proof_type!=DECLARED
    own=prove('<title>Example AS</title><footer>© Example AS '+credit.replace('Example AS','Agency AS')+'</footer>')
    assert own.proof_type==DECLARED


def test_only_case_spacing_and_norwegian_letters_normalised():
    assert name_fragment(page('<footer>ÆØÅ   AS</footer>'),'aeoa as')
    assert not name_fragment(page('<footer>Café AS</footer>'),'Cafe AS')
    assert not name_fragment(page('<footer>Example & Sons AS</footer>'),'Example og Sons AS')


def test_cross_domain_redirect_needs_explicit_registry_domain_or_publisher_number():
    context={'name':'Example AS','website':'example.no','candidate_url':'https://www.example.no/'}
    target=page('<footer>Example AS</footer>','https://other.no/')
    assert not declared_receipt(target,ORG,context)
    assert declared_receipt(target,ORG,{**context,'email':'contact@other.no'})
    assert declared_receipt(page(f'<footer>Example AS {ORG}</footer>','https://other.no/'),ORG,context)
    assert not declared_receipt(target,ORG,{**context,'candidate_url':'https://unrelated.no/'})


def test_old_high_contact_gate_does_not_override_new_declared_name_rule():
    p=prove('<title>Example AS</title><footer>Example AS; Exampleveien 1</footer>',street='Exampleveien 1')
    assert p.level=='HIGH' and p.proof_type==DECLARED


def test_punctuation_in_full_name_localizes_new_tier_when_old_high_token_does_not(tmp_path,monkeypatch):
    from signalpost.web.publisher_identity import localized_span
    p=page('<title>Example & Sons AS</title><footer>Example & Sons AS; Exampleveien 1; Telefon 12345678</footer>')
    context={'name':'Example & Sons AS','website':'example.no','street':'Exampleveien 1','phone':'12345678'}
    proof=candidate_proof(p,ORG,context,Candidate('https://example.no/','example.no','registry_website'),[])
    assert proof.level=='HIGH' and proof.proof_type==DECLARED
    assert 'Example & Sons AS' in localized_span(p,proof.publisher_receipt)


@pytest.mark.parametrize('footer', ['Example AS Org.nr 993578843','Example AS is part of Example Group',
                                  'Example AS; domain is parked','Example AS; buy this domain',
                                  'Example AS; Example IKS'])
def test_conflicts_precede_new_positive_tier(footer):
    assert prove('<footer>'+footer+'</footer>').level=='REJECT'


def test_publication_keeps_registry_and_publisher_receipts(tmp_path,monkeypatch):
    from tests.test_websites import execute_web, html
    from scripts.verify_output import verify
    _, row, _, cfg = execute_web(tmp_path,monkeypatch,body=html('© Example AS'))
    c=next(c for c in row['claims'] if c['field']=='official_website')
    assert c['value']['proof_type']==DECLARED
    evidence={e['id']:e for e in row['evidence']}
    assert any(evidence[e]['source_class']=='official_registry' for e in c['evidence_ids'])
    verify(cfg.output,cfg.state_dir,1)


def test_registry_redirect_obeys_destination_robots_and_exact_publisher_requirement(tmp_path,monkeypatch):
    import httpx
    from tests.test_websites import execute_web,html
    for kind in ('blocked','name_only','body_number','publisher_number'):
        def respond(request):
            if request.url.path=='/robots.txt':
                return httpx.Response(200,text='User-agent: *\nDisallow: /' if kind=='blocked' and request.url.host=='other.no' else 'User-agent: *\nAllow: /')
            if request.url.host=='example.no':
                return httpx.Response(301,headers={'location':'https://other.no/'})
            if request.url.host!='other.no':return httpx.Response(404,text='missing')
            return httpx.Response(200,text=html(f'Example AS {ORG}' if kind=='publisher_number' else 'Example AS',extra=f'<p>{ORG}</p>' if kind=='body_number' else ''))
        _,row,requests,cfg=execute_web(tmp_path/kind,monkeypatch,response=respond)
        sites=[c for c in row['claims'] if c['field']=='official_website']
        # R6b explicitly authorizes the full publisher legal name on a
        # declared redirect destination; destination robots still veto first.
        assert bool(sites)==(kind!='blocked')
        if kind=='blocked':assert 'https://other.no/' not in requests
        assert len([u for u in requests if 'data.brreg.no' not in u])<=13


def test_forged_registry_or_publisher_receipt_fails_verifier(tmp_path,monkeypatch):
    import json
    from tests.test_websites import execute_web,html
    from scripts.verify_output import verify
    _,row,_,cfg=execute_web(tmp_path,monkeypatch,body=html('© Example AS'))
    site=next(c for c in row['claims'] if c['field']=='official_website')
    site['value']['publisher_identity']['publisher_excerpt']='Forged AS'
    cfg.output.write_text(json.dumps(row)+'\n',encoding='utf8')
    with pytest.raises(AssertionError):verify(cfg.output,cfg.state_dir,1)


def test_url_cannot_be_replaced_while_reusing_valid_publisher_proof(tmp_path,monkeypatch):
    import json
    from tests.test_websites import execute_web,html
    from scripts.verify_output import verify
    _,row,_,cfg=execute_web(tmp_path,monkeypatch,body=html('© Example AS'))
    site=next(c for c in row['claims'] if c['field']=='official_website')
    site['value']['final_url']='https://unrelated.no'
    cfg.output.write_text(json.dumps(row)+'\n',encoding='utf8')
    with pytest.raises(AssertionError):verify(cfg.output,cfg.state_dir,1)
