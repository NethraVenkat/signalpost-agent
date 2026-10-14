"""Pure header scoring in one CPU process; no HTTP, state files or credentials."""
from concurrent.futures import ProcessPoolExecutor
from .nav import header_name,name_tokens,name_matches,distinctive_tokens

POOL=ProcessPoolExecutor(max_workers=1)


def score_many(headers,names,token_orgs,frequency,active_count,unfiltered,ranked):
    result={}
    for uuid,name in headers:
        if unfiltered or not name:result[uuid]=(0,set(names));continue
        if not ranked:
            result[uuid]=(0,{org for org,known in names.items() if any(name_matches(name,c) for c in known)})
            continue
        tokens=distinctive_tokens(name,frequency,active_count)
        possible=set().union(*(token_orgs.get(t,set()) for t in tokens)) if tokens else set()
        affected={org for org in possible if any(name_matches(name,c) for c in names[org])}
        score=max((sum(1/max(1,frequency[t]) for t in sorted(tokens & name_tokens(c)))
            for org in affected for c in names[org]),default=0)
        result[uuid]=(score,affected)
    return result
