"""Fail-closed sentence checks over a bounded, evidence-backed claim catalog."""
import re
from datetime import date
from decimal import Decimal,InvalidOperation
from .catalog import catalog,leaves
from ..models.synthesis import Sentence,Unknown
from .readability import headline,nace_sentence,dual_role,normalised_description,money,workplaces_sentence
from .nace import unspecified

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
    without_urls=re.sub(r'\bFY(\d{4})\b',r'\1',without_urls)
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
    # These new frames are checked in full, bound to every claim they use.
    # Table titles authorize only the matching NACE frame or headline.
    plain=sentence.text.removeprefix('Previously supported. ')
    opening=headline(claims)
    opening_matches=opening and sentence.text==opening[0]
    municipality=next((c for c in claims if c.field=='identity.municipality'),None)
    if opening and municipality and not opening_matches and ' is based in ' in opening[0]:
        start=opening[0].index(' is based in ')+len(' is based in ')
        end=start+len(str(municipality.value).title())
        city=sentence.text[start:end]
        opening_matches=city.casefold()==str(municipality.value).casefold() and sentence.text==headline(claims,municipality_display=city)[0]
    if opening_matches:
        if set(sentence.claim_ids)!=set(opening[1]):return 'misbound_headline'
        if sentence.value_kind!='reported' or sentence.count is not None or sentence.record_type is not None:return 'unmarked_derived_count'
        return None
    outside_quotes=re.sub(r'«.*?»',' ',plain,flags=re.S)
    if ' is a ' in outside_quotes or ' is based in ' in outside_quotes or 'registered under ' in outside_quotes or outside_quotes.startswith('Registered name: ') or ' registered employees' in outside_quotes or ' in revenue in FY' in outside_quotes:
        return 'unverified_headline'
    if plain.startswith('NACE '):
        if len(claims)!=1 or not claims[0].field.startswith('identity.nace') or unspecified(claims[0].value) or sentence.text!=nace_sentence(claims[0]):return 'unverified_nace_title'
        if sentence.value_kind!='reported' or sentence.count is not None or sentence.record_type is not None:return 'unmarked_derived_count'
        return None
    if ' is both CEO and chair.' in plain:
        if any(not c.field.startswith('roles.role.') or c.value.get('inactive') is True for c in claims):return 'misbound_role'
        merged=dual_role(claims)
        if not merged or sentence.text!=merged[0] or set(sentence.claim_ids)!=set(merged[1]):return 'misbound_role'
        if sentence.value_kind!='reported' or sentence.count is not None or sentence.record_type is not None:return 'unmarked_derived_count'
        return None
    if plain.startswith('Registered activity and purpose: '):
        fields={c.field:c for c in claims}
        if set(fields)!={'identity.registered_activity','identity.statutory_purpose'} or len(claims)!=2:return 'misbound_activity'
        activity=fields['identity.registered_activity'];purpose=fields['identity.statutory_purpose']
        value=normalised_description(activity.value)
        prefix='Previously supported. ' if activity.carried_forward or purpose.carried_forward else ''
        if value!=normalised_description(purpose.value) or sentence.text!=prefix+'Registered activity and purpose: «'+value[:300]+'».':return 'non_verbatim_quote'
        if sentence.value_kind!='reported' or sentence.count is not None or sentence.record_type is not None:return 'unmarked_derived_count'
        return None
    if plain in {'First observation; no earlier run to compare.','No changes since the previous run.'}:
        refresh=getattr(getattr(envelope,'run',None),'refresh',{})
        baseline=refresh.get('mode')=='baseline'
        if (plain.startswith('First observation') and not baseline) or (plain.startswith('No changes') and (baseline or envelope.changes)):return 'unverified_refresh_notice'
    # Money can cite only the exact account amount, not a year or another
    # numeric value in the same citation. Reject abbreviated/rounded amounts.
    if re.search(r'\b(?:million|billion|thousand)\b',plain,re.I):return 'unverified_number'
    for match in re.finditer(r'\b(NOK|EUR|USD|SEK|DKK|GBP)\s+([-+]?\d[\d, .\u00a0]*\d|[-+]?\d)',plain):
        rendered=match.group(2).strip().rstrip('.')
        if not any(c.field.startswith('accounts.') and isinstance(c.value,(int,float)) and
                   (getattr(c,'reporting_period',None) or {}).get('currency')==match.group(1) and
                   number(rendered)==number(str(c.value)) and
                   re.sub(r'\D','',rendered)==re.sub(r'\D','',money(c.value)) for c in claims):return 'unverified_number'
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
        if sentence.record_type=='workplaces':
            all_units={c.id for c in envelope.claims if c.availability=='available' and matches(c)}
            if len(claims)!=len(records) or records!=all_units or sentence.text!=workplaces_sentence(claims):return 'unverified_derived_count'
            return None
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
