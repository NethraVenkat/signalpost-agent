from signalpost.synthesis.brief import select


def test_overview_prioritizes_supported_topics_without_hiding_jobs_and_activity():
    fields = ['identity.nace1', 'roles.role.1', 'identity.municipality', 'accounts.revenue',
              'hiring.job.1', 'dated_item.1', 'identity.legal_name', 'website_description.about']
    claims = [{'id': str(i), 'field': f, 'availability': 'available'} for i, f in enumerate(fields)]
    sentences = [{'text': f, 'claim_ids': [str(i)]} for i, f in enumerate(fields)]
    synthesis = {'sections': {'what_it_does': [sentences[0], sentences[7]] * 4,
                              'leadership': [sentences[1]], 'scale': sentences[2:5],
                              'changes': sentences[5:7]}}
    result = select(synthesis, claims)
    assert len(result) == 8
    assert result[4]['claim_ids'] == ['4'] and result[5]['claim_ids'] == ['5']
    assert len({s['text'] for s in result}) == 8


def test_sparse_or_unsupported_summary_is_never_padded():
    assert select({'sections': {'scale': [{'text': 'Unsupported', 'claim_ids': ['missing']}]}}, []) == []
