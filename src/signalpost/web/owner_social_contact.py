"""One linked own contact page after website proof, within existing caps."""
import asyncio,re,time
from urllib.parse import urlsplit
from ..budget import SourceFailure
from ..workers import offload
from .html import Page
from .policy import domain
from .publisher_veto import conflict

CONTACT=re.compile(r'(?:^|/)(?:kontakt(?:[-_].*)?|contact(?:[-_].*)?|impressum|imprint)(?:/|\.|$)',re.I)

async def collect(org,choice,http,proved,context):
    candidate,proof,response,page,pages=choice
    status={'state':'not_available','checked_urls':[],'errors':[],'scope':'One visible own navigation/footer contact/imprint link after verified/HIGH website proof; existing cumulative budgets'}
    if proof.level not in {'HIGH','VERIFIED'} or proof.other_orgnrs:return [],status
    seen={r.url for r,p in pages};targets=[]
    for r,p in pages:
        for link in p.links:
            if not link.visible_context or not link.owned_context or domain(link.href)!=domain(response.url) or not CONTACT.search(urlsplit(link.href).path):continue
            if link.href not in seen and link.href not in targets:targets.append(link.href)
    if not targets:return [],status
    target=targets[0]
    try:
        extra=await http.get(target,org,domain(response.url),proved)
        status['checked_urls'].append(target)
        if extra.status!=200:
            status.update(state='failed',errors=['http_'+str(extra.status)]);return [],status
        if domain(extra.url)!=domain(response.url) or not CONTACT.search(urlsplit(extra.url).path):
            status.update(state='blocked',errors=['social_contact_redirect_refused']);return [],status
        parsed=await offload(Page,extra.body,extra.url)
        blocked=await offload(lambda:conflict(parsed,org,context)[0])
        if blocked:
            status.update(state='blocked',errors=['social_contact_publisher_conflict']);return [],status
        status['state']='available';return [(extra,parsed)],status
    except asyncio.CancelledError:
        if time.monotonic()<getattr(getattr(http,'budget',None),'deadline',float('inf')):raise
        status.update(state='failed',errors=['deadline']);return [],status
    except SourceFailure as exc:
        status.update(state='failed',errors=[exc.code]);return [],status
