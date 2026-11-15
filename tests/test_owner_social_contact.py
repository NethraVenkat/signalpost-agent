import asyncio
from types import SimpleNamespace
import pytest
from signalpost.web.html import Page
from signalpost.budget import SourceFailure
from signalpost.web import owner_social_contact as m
ORG='986464492'
def check(raw,extra='',fail=None,group=False,final='https://example.no/kontakt'):
    page=Page(raw.encode(),'https://example.no/');response=SimpleNamespace(url=page.url)
    calls=[]
    class Http:
        async def get(self,url,*args):
            calls.append(url)
            if fail:raise SourceFailure(fail)
            return SimpleNamespace(status=200,url=final,body=extra.encode())
    proof=SimpleNamespace(level='VERIFIED',other_orgnrs=['995194163'] if group else [])
    result=asyncio.run(m.collect(ORG,(None,proof,response,page,[(response,page)]),Http(),[],{'name':'EXAMPLE AS'}))
    return result,calls
def test_own_navigation_link_one_request():
    (pages,state),calls=check('<nav><a href="/kontakt">Kontakt</a><a href="/contact">Contact</a></nav>','<footer>Telefon 12345678 F?lg oss</footer>')
    assert calls==['https://example.no/kontakt'] and len(pages)==1 and state['state']=='available'
@pytest.mark.parametrize('raw',['<article><a href="/kontakt">Kontakt</a></article>','<nav hidden><a href="/kontakt">Kontakt</a></nav>','<nav><a href="https://foreign.no/kontakt">Kontakt</a></nav>','<main><a href="/kontakt">Kontakt</a></main>'])
def test_nonowner_links_not_fetched(raw):
    (_,state),calls=check(raw)
    assert not calls and state['state']=='not_available'
def test_group_site_not_fetched():
    (_,state),calls=check('<footer><a href="/kontakt">Kontakt</a></footer>',group=True)
    assert not calls
def test_budget_failure_explicit_without_losing_website():
    (pages,state),calls=check('<footer><a href="/kontakt">Kontakt</a></footer>',fail='website_budget_exhausted')
    assert not pages and state['errors']==['website_budget_exhausted'] and len(calls)==1
def test_foreign_publisher_rejected():
    (pages,state),calls=check('<nav><a href="/kontakt">Kontakt</a></nav>','<footer>OTHER AS Org.nr 995194163</footer>')
    assert not pages and state['errors']==['social_contact_publisher_conflict']
def test_foreign_redirect_rejected():
    (pages,state),calls=check('<nav><a href="/kontakt">Kontakt</a></nav>',final='https://foreign.no/kontakt')
    assert not pages and state['errors']==['social_contact_redirect_refused']

def test_deadline_cancellation_preserves_completed_website_proof():
    import time
    page=Page(b'<nav><a href="/kontakt">Kontakt</a></nav>','https://example.no/')
    response=SimpleNamespace(url=page.url);proof=SimpleNamespace(level='VERIFIED',other_orgnrs=[])
    class Http:
        budget=SimpleNamespace(deadline=time.monotonic()-1)
        async def get(self,*args):raise asyncio.CancelledError()
    pages,state=asyncio.run(m.collect(ORG,(None,proof,response,page,[(response,page)]),Http(),[],{'name':'EXAMPLE AS'}))
    assert not pages and state['errors']==['deadline'] and proof.level=='VERIFIED'
