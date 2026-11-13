"""Official available-copy years; no PDF downloads or guessed accounting units."""
import re
from ..budget import SourceFailure
from .extract import Section,add,decode,finish,response_source

YEARS='https://data.brreg.no/regnskapsregisteret/regnskap/aarsregnskap/kopi/{org}/aar'


def extract(org,response):
    data,error=decode(response,'accounts')
    if error:
        add(error,response_source(response),org,'accounts','accounts.filed_years',None,'/',
            availability=error.state,method='signalpost.accounts_years.v1')
        return error
    if response.url!=YEARS.format(org=org):raise SourceFailure('wrong_company','Filing-years endpoint differs from requested entity')
    if not isinstance(data,list) or any(not isinstance(y,str) or not re.fullmatch(r'[0-9]{4}',y) for y in data):
        raise SourceFailure('malformed_filing_years')
    result=Section();source=response_source(response)
    years=sorted(set(data),reverse=True)
    add(result,source,org,'accounts','accounts.filed_years',years,'/',method='signalpost.accounts_years.v1')
    result.claims[-1].reasons['scope']='Years for which the official API offers an annual-accounts copy; not complete lifetime filing history'
    for year in years:
        add(result,source,org,'accounts','accounts.filed_year.'+year,year,'/'+str(data.index(year)),method='signalpost.accounts_years.v1')
    return finish(result)
