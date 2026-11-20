# Website publisher receipts

The two trial contradictions came from the legacy `HIGH` heuristic. It returned `proof_type=signals` before the collector could construct a publisher identity receipt. The precision verifier could read each claim's own span and hash but could not replay publisher attribution from that proof type. The legacy heuristic now supplies diagnostics only. Exact organisation-number proofs still take precedence. A `HIGH` result must pass one of the existing publisher receipt rules.

| Organisation | Claim | Stored SHA-256 | Locator | Excerpt of cited span |
|---|---|---|---|---|
| `989087126` | `post@aretorevisjon.no` | `1f664cdb8c82a8e231b8ed1f941e14d802a621426a82db6d917ab7012a2e022c` | `contact:post@aretorevisjon.no` | `<span class="elementor-icon-list-text">post@aretorevisjon.no</span>` |
| `975978729` | `https://kistefosmobler.no` | `38bb4139565f130ad1f19909dcf7512f17619ac992d45935048859e946192643` | `identity-proof:975978729` | `<link rel="canonical" href="https://kistefosmobler.no/" />` |

The first blob is the homepage at `https://www.aretorevisjon.no/`, fetched at `2026-11-20T15:29:43.572425Z`. The span establishes that the site published the address. A complete publisher receipt ties the site's full legal name to the registry-declared domain. The address also equals the registry email. The email claim passes with that owner proof.

The second blob is the homepage at `https://kistefosmobler.no/`, fetched at `2026-11-20T15:29:59.060328Z`. The canonical link establishes the URL. The cited title uses the company name without its legal suffix. The existing `registry_declared_live` rule matches the exact registry domain and the unique registered name core in the publisher title, after checking for conflicting publisher identities. The website claim now carries that receipt and passes. The same extractor version, `signalpost.website.v1`, was recorded on both cited spans.

The exact original spans are recorded below as JSON strings, including escaped indentation and truncated tag boundaries from the original receipts.

```json
{
  "989087126": "\t<span class=\"elementor-icon-list-text\">post@aretorevisjon.no</span>\n\t\t\t\t\t\t\t\t\t</li>\n\t\t\t\t\t\t</ul>\n\t\t\t\t\t\t</div>\n\t\t\t\t</div>\n\t\t\t\t\t</div>\n\t\t</div>\n\t\t\t\t\t</di",
  "975978729": "roduct/yoast-seo-wordpress/ -->\n\t<title>Kistefos møbler - Kjøkken og kvalitetsmøbler - Kistefos Møbler</title>\n\t<link rel=\"canonical\" href=\"https://kistefosmobler.no/\" />\n\t<meta property=\"og:locale\" content=\"nb_NO\" />\n\t<meta property=\"og:type\" content=\"website\" />\n\t<meta property=\"og:title\" content="
}
```

The corrected rule was replayed on all 500 Stage 2 envelopes with zero HTTP requests. Three websites used the legacy heuristic. Two were reissued with publisher receipts. The third, `999582214`, lacked a publishable receipt under the default settings. Seven other claims were withdrawn, comprising its website and six dependent descriptions. Available website coverage went from 38 to 37. The 31 websites labelled `VERIFIED` were retained. All 500 profiles were rebuilt, with a largest HTML file of 234,189 bytes.

The updated 200-claim stored-evidence draw at seed `202611200628` yielded **199 supported**, **1 contradicted** and **0 missing or mismatched blobs**. The Wilson 95% lower bound was **97.22%**, above the 95% gate. The remaining audit disagreement is a phone number shown with spaces in a text span that the sampler checks as an unspaced literal. Both reported claims passed a separate targeted check using their saved blobs.

The 500-company checker passed with 76,888 claims and zero unsupported synthesis or briefing values. All 1,524 collected tests passed across four batches, including the rerun of a timer-resolution test that had failed its wall-clock assertion. The corrected test uses the cancellation handshake to verify that exact-ID work continues. The separate privacy and profile checks passed 17 and 2 tests, respectively.
