import httpx
from tests.test_registry import execute,config,handler

ORG='923609016'


def failed(request):
    if request.url.path.endswith('/roller'): raise httpx.ReadTimeout('synthetic',request=request)
    return handler()(request)


def empty(request):
    if request.url.path.endswith('/roller'):return httpx.Response(200,json={'organisasjonsnummer':ORG,'rollegrupper':[]})
    return handler()(request)


def test_failed_to_checked_absence_is_observation(tmp_path):
    first=config(tmp_path/'first',[ORG]); execute(first,failed)
    report,rows=execute(config(tmp_path/'second',[ORG],previous=first.output),empty)
    assert report['changes']==0 and report['observation_changes']==1
    change=rows[0]['run']['refresh']['observation_changes'][0]
    assert change['section']=='roles' and change['previous_state']=='failed' and change['current_state']=='not_available'


def test_checked_removal_is_a_company_change(tmp_path):
    first=config(tmp_path/'first',[ORG]); execute(first)
    report,rows=execute(config(tmp_path/'second',[ORG],previous=first.output),empty)
    assert report['changes']==1 and report['observation_changes']==0
    assert rows[0]['changes'][0]['field']=='roles.roles'


def test_same_failed_source_is_idempotent(tmp_path):
    first=config(tmp_path/'first',[ORG]); execute(first,failed)
    report,_=execute(config(tmp_path/'second',[ORG],previous=first.output),failed)
    assert report['changes']==0 and report['observation_changes']==0


def test_ambiguity_carries_supported_claims_and_resolving_is_observation(tmp_path):
    first=config(tmp_path/'first',[ORG]); execute(first)
    def wrong(request):
        if request.url.path.endswith('/roller'):return httpx.Response(200,json={'organisasjonsnummer':'993578843','rollegrupper':[]})
        return handler()(request)
    second=config(tmp_path/'second',[ORG],previous=first.output)
    report,rows=execute(second,wrong)
    assert report['changes']==0 and report['observation_changes']==1
    assert any(c['family']=='roles' and c['carried_forward'] for c in rows[0]['claims'])
    report,_=execute(config(tmp_path/'third',[ORG],previous=second.output))
    assert report['changes']==0 and report['observation_changes']==1


def test_disabled_website_is_not_a_company_removal(tmp_path,monkeypatch):
    from tests.test_websites import execute_web
    _,_,_,first=execute_web(tmp_path/'web',monkeypatch)
    report,rows=execute(config(tmp_path/'registry',[ORG],previous=first.output))
    assert not any(c['field']=='official_website' for c in rows[0]['changes'])
