"""Classify access gates, not ordinary protected contact forms."""
import re


def detected(page):
    raw=page.raw.casefold();title=page.title.casefold();visible=page.visible.casefold()
    if any(token in raw for token in ('cf-chl-','checking your browser','verify you are human')):return True
    # Cloudflare's passive JSD is also injected into fully usable sites. It is
    # not an access gate; active orchestrators and visible gates still block.
    if re.search(r'/cdn-cgi/challenge-platform/(?!scripts/jsd/)',raw):return True
    if re.search(r'captcha|challenge',title):return True
    vendors=('cloudflare','datadome','captcha-delivery.com','_incapsula_resource','incapsula','imperva','perimeterx','ddos-guard','sucuri','akamai','awswaf')
    gate=re.search(r'just a moment|access denied|access restricted|attention required|security (?:check|verification)|request unsuccessful|checking (?:your|the) browser|enable javascript and cookies|one more step|human verification',title+' '+visible[:1500])
    return bool(gate and any(marker in raw for marker in vendors))
