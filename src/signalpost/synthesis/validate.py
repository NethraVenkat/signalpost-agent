"""Fail-closed sentence checks over a bounded, evidence-backed claim catalog."""
import re
from datetime import date
from decimal import Decimal,InvalidOperation
from .catalog import catalog,leaves
from ..models.synthesis import Sentence,Unknown

SECTIONS=('what_it_does','scale','leadership','changes')
LEVELS={'VERIFIED','HIGH','REGISTRY_DECLARED'}
FIXED_WORDS=set('Registered activity purpose NACE Website Self description Employees Reported revenue Annual result Fiscal year Municipality Workplaces Board members Verified active ads found Official website Social profile CEO Chair Auditor First observation no earlier run to compare Previous Current Change From To Bankruptcy Liquidation Deletion Registration date Previously supported As registered NOK FY English CEO'.casefold().split())
DATE=re.compile(r'\b(?:\d{4}[-/]\d{2}[-/]\d{2}|\d{1,2}[/.]\d{1,2}[/.]\d{4})\b')
NUMBER=re.compile(r'(?<![\w])[-+]?\d+(?:[ ,\u00a0]\d{3})*(?:\.\d+)?(?:[eE][+-]?\d+)?(?![\w])')
URL=re.compile(r'https?://[^\s<>«»]+')
NAME=re.compile(r'\b[A-ZÆØÅ][\wÆØÅæøå-]*(?:\s+[A-ZÆØÅ][\wÆØÅæøå-]*)*')


def number(value):
    try:return str(Decimal(value.replace(',','').replace(' ','').replace('\u00a0','')).normalize())
    except InvalidOperation:return None


def date_token(value):
    try:
        if re.match(r'^\d{4}',value):parts=[int(x) for x in re.split('[-/]',value)]
        else:
            day,month,year=[int(x) for x in re.split('[/.]',value)];parts=[year,month,day]
        return date(*parts).isoformat()
    except (ValueError,TypeError):return None


def tokens(text):
    dates={date_token(m.group()) for m in DATE.finditer(text)}
    without_dates=DATE.sub(' ',text)
    urls={m.group().rstrip('.,;') for m in URL.finditer(text)}
    without_urls=URL.sub(' ',without_dates)
    nums={number(m.group()) for m in NUMBER.finditer(without_urls)}
    return dates-{None},nums-{None},urls


def claim_strings(claim):
    strings=list(leaves(claim.value))
    if getattr(claim,'reporting_period',None):strings+=list(leaves(claim.reporting_period))
    return strings


def permitted(claim,envelope):
    if getattr(claim,'family',None)=='website':
        if claim.field=='official_website':return isinstance(claim.value,dict) and claim.value.get('identity_level') in LEVELS
        if claim.field.startswith('website_description.'):
            parent=next((c for c in envelope.claims if c.id==claim.value.get('identity_claim_id')),None)
            return bool(parent and parent.availability=='available' and parent.field=='official_website' and permitted(parent,envelope))
        parent=next((c for c in envelope.claims if c.field=='official_website' and c.availability=='available'),None)
        return bool(parent and permitted(parent,envelope))
    return True


def sentence_error(sentence,envelope):
    available=catalog(envelope)
    if not sentence.claim_ids:return 'uncited_sentence'
    if any(key not in available for key in sentence.claim_ids):return 'missing_or_unavailable_claim'
    claims=[available[key] for key in sentence.claim_ids]
    evidence={e.id for e in envelope.evidence}
    if any(not c.evidence_ids or set(c.evidence_ids)-evidence for c in claims):return 'missing_evidence'
    if any(not permitted(c,envelope) for c in claims):return 'identity_below_threshold'
    derived=None
    if sentence.value_kind=='derived':
        def matches(claim):
            if not getattr(claim,'family',None):return False
            if sentence.record_type=='workplaces':return claim.family=='subunits' and claim.field.startswith('subunits.unit.')
            if sentence.record_type=='active_ads':return claim.family=='hiring' and claim.field.startswith('hiring.job.') and not claim.carried_forward
            if sentence.record_type=='board_members':
                return claim.family=='roles' and isinstance(claim.value,dict) and (claim.value.get('group_type') or {}).get('kode')=='STYR' and (claim.value.get('role_type') or {}).get('kode') in {'LEDE','NEST','MEDL'} and claim.value.get('inactive') is not True
            return False
        records={c.id for c in claims if matches(c)}
        if sentence.count is None or sentence.count<=0 or sentence.count!=len(records):return 'unverified_derived_count'
        labels={'workplaces':'Registered workplaces','board_members':'Registered board members','active_ads':'Verified active ads found'}
        if sentence.text!=labels[sentence.record_type]+': '+str(sentence.count)+'.':return 'unverified_derived_count'
        derived=number(str(sentence.count))
    elif sentence.count is not None or sentence.record_type is not None:return 'unmarked_derived_count'
    strings=[text for claim in claims for text in claim_strings(claim)]
    for quoted in re.findall(r'«(.*?)»',sentence.text,re.S):
        if not any(quoted in value for value in strings):return 'non_verbatim_quote'
    expected=[tokens(text) for text in strings]
    actual=tokens(sentence.text)
    for index,label in enumerate(('date','number','url')):
        supported=set().union(*(item[index] for item in expected)) if expected else set()
        if index==1 and derived is not None:supported.add(derived)
        if actual[index]-supported:return 'unverified_'+label
    # Proper-name tokens must be present in cited values, never merely plausible.
    outside_quotes=re.sub(r'«.*?»',' ',sentence.text,flags=re.S)
    outside_quotes=URL.sub(' ',outside_quotes)
    supported_words={word.casefold() for text in strings for word in re.findall(r'[\wÆØÅæøå-]+',text)}
    for match in NAME.finditer(outside_quotes):
        if any(word.casefold() not in FIXED_WORDS|supported_words for word in match.group().split()):return 'unverified_name'
    return None


def validate_synthesis(synthesis,envelope):
    rejected=[]
    for section in SECTIONS:
        sentences=getattr(synthesis.sections,section);valid=[]
        for raw in sentences:
            sentence=raw if isinstance(raw,Sentence) else Sentence.model_validate(raw)
            reason=sentence_error(sentence,envelope)
            if reason:rejected.append({'section':section,'reason':reason})
            else:valid.append(sentence)
        setattr(synthesis.sections,section,valid)
        if sentences and not valid:
            synthesis.sections.unknowns.append(Unknown(family=section,state='failed',reason='No sentence passed evidence validation.'))
    total=sum(len(getattr(synthesis.sections,key)) for key in SECTIONS)
    synthesis.checks.sentences=synthesis.checks.cited=total
    synthesis.checks.values_verified=True
    synthesis.checks.dropped_sentences+=len(rejected)
    synthesis.checks.rejections.extend(rejected)
    synthesis.summary=' '.join(s.text for key in SECTIONS for s in getattr(synthesis.sections,key))
    return synthesis
