"""Descriptive arithmetic only; no forecasts, scale conversion or suitability claims."""
import re
from datetime import date
from decimal import Decimal, DecimalException, ROUND_HALF_UP, localcontext
from ..models.synthesis import FinancialMetric, Sentence

LABELS = {'operating_margin':'operating margin', 'equity_ratio':'equity ratio', 'revenue_yoy':'revenue change'}


def amount(claim):
    if claim is None or isinstance(claim.value, bool) or not isinstance(claim.value, (int, float)):
        return None
    value = Decimal(str(claim.value))
    return value if value.is_finite() else None


def period(claim, require_unit=True):
    p = claim.reporting_period or {}
    try:
        start, end = date.fromisoformat(p['period_start']), date.fromisoformat(p['period_end'])
        if start > end or str(end.year) != str(p.get('fiscal_year')) or p.get('account_type') != 'SELSKAP': return None
    except (KeyError, TypeError, ValueError): return None
    if require_unit and (not isinstance(p.get('unit'),str) or not p['unit'] or not re.fullmatch(r'[A-Z]{3}',str(p.get('currency','')))):
        return None
    return {k:p.get(k) for k in ('fiscal_year','period_start','period_end','currency','unit','account_type')}


def comparable(current, previous):
    a,b = period(current), period(previous)
    if not a or not b: return False
    if any(a[k] != b[k] for k in ('currency','unit','account_type')): return False
    sa,ea,sb,eb = [date.fromisoformat(p[k]) for p,k in [(a,'period_start'),(a,'period_end'),(b,'period_start'),(b,'period_end')]]
    return (ea.year == eb.year+1 and sa.year == sb.year+1
            and (sa.month,sa.day,ea.month,ea.day)==(sb.month,sb.day,eb.month,eb.day)
            and 350 <= (ea-sa).days+1 <= 366 and 350 <= (eb-sb).days+1 <= 366
            and eb < sa)


def percentage(numerator, denominator):
    if numerator is None or denominator is None or denominator <= 0: return None
    try:
        with localcontext() as ctx:
            ctx.prec = 80
            result = (numerator / denominator * 100).quantize(Decimal('.01'), rounding=ROUND_HALF_UP)
            return format(result,'f') if result.is_finite() else None
    except DecimalException: return None


def analyze(envelope):
    claims = [c for c in envelope.claims if c.family=='accounts' and c.availability=='available']
    current = {c.field:c for c in claims if not c.field.startswith('accounts.history.')}
    metrics=[]; gaps={}
    for formula,top,bottom in [('operating_margin','operating_result','revenue'),('equity_ratio','equity','total_assets')]:
        a,b = current.get('accounts.'+top),current.get('accounts.'+bottom)
        if a is None or b is None: gaps[formula]='missing supported inputs'; continue
        pa,pb = period(a),period(b)
        if not pa or pa != pb: gaps[formula]='unverified or mismatched period, currency, unit or entity scope'; continue
        value=percentage(amount(a),amount(b))
        if value is None: gaps[formula]='non-finite inputs or non-positive denominator'; continue
        metrics.append(FinancialMetric(formula=formula,value=value,input_claim_ids=[a.id,b.id],reporting_period=pa,
                                       carried_forward=a.carried_forward or b.carried_forward))
    revenue=current.get('accounts.revenue')
    previous=sorted((c for c in claims if c.field.startswith('accounts.history.') and c.field.endswith('.revenue')),
                    key=lambda c:str((c.reporting_period or {}).get('period_end','')),reverse=True)
    prior=next((c for c in previous if revenue and comparable(revenue,c)),None)
    if not revenue or not prior: gaps['revenue_yoy']='two comparable annual entity periods are not supported'
    else:
        now,old=amount(revenue),amount(prior)
        value=percentage(now-old if now is not None and old is not None else None,old)
        if value is None: gaps['revenue_yoy']='non-finite inputs or non-positive prior revenue'
        else: metrics.append(FinancialMetric(formula='revenue_yoy',value=value,input_claim_ids=[revenue.id,prior.id],
                 reporting_period=period(revenue),previous_period=period(prior),carried_forward=revenue.carried_forward or prior.carried_forward))
    registered=next((c for c in envelope.claims if c.field=='identity.latest_submitted_accounts' and c.availability=='available'),None)
    figure=next((c for c in sorted(current.values(),key=lambda c:c.field) if period(c,False)),None)
    year_check=None
    if registered and not isinstance(registered.value,bool) and re.fullmatch(r'\d{4}',str(registered.value)) and figure:
        registered_year=str(registered.value); figures_year=period(figure,False)['fiscal_year']
        year_check={'newer_filing_exists':int(registered_year)>int(figures_year),'registry_year':registered_year,
                    'figures_year':figures_year,'claim_ids':[registered.id,figure.id],
                    'scope':'Registry year comparison only; same-year refilings are not checked.'}
    return metrics,year_check,gaps


def metric_sentence(metric):
    prefix='Derived from previously supported figures: ' if metric.carried_forward else 'Derived '
    if metric.formula=='revenue_yoy':
        text=prefix+'revenue change from FY'+metric.previous_period['fiscal_year']+' to FY'+metric.reporting_period['fiscal_year']+': '+metric.value+'%.'
    else: text=prefix+LABELS[metric.formula]+' for FY'+metric.reporting_period['fiscal_year']+': '+metric.value+'%.'
    return Sentence(text=text,claim_ids=metric.input_claim_ids,value_kind='derived',formula=metric.formula)
