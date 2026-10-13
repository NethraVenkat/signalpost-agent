"""Factual calibration records; no arithmetic is applied to published metrics."""
from ..models.evidence import utc_now
from .extract import Section, Source, add

CALIBRATIONS=[
    ('https://www.tomra.com/-/media/project/tomra/tomra/investor-relations/annual-reports/2025/tomra-annual-report-2025.pdf',
     'fe379ce4f1ee133068b59c82fd1a7e25bc72c1459ba9e91a02d6621f2466414a','pdf:page145:parent-income-statement:2025',
     'Amounts in NOK million\n2025\nOperating revenues 3,546.3\nProfit for the period 510.4\n'),
    ('https://www.akersolutions.com/globalassets/investors/agm/2026/aker-solutions-annual-report-2025.pdf',
     'c0e145933ff95654d05faed3b45b2eab327aa9d5ff712eeac5adad22f528f7ba','pdf:page176:parent-income-statement:2025',
     'Amounts in NOK million\n2025\nOperating revenues 53\nNet income (loss) 4,063\n')]


def evidence(blobs):
    result=[]
    for url,pdf_sha,locator,text in CALIBRATIONS:
        body=text.encode('utf8'); sha=blobs.put(body)
        source=Source(url,body,sha,utc_now(),url+'#pdf_sha256='+pdf_sha)
        temporary=Section()
        add(temporary,source,'calibration','calibration','unit', 'NOK',locator,span=text[:300],source_class='company_report',method='signalpost.pdf_calibration.v1')
        result.extend(temporary.evidence)
    return result
