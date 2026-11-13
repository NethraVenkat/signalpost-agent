# R1 publisher context

The independent local extractor in signalpost.web.publisher returns labelled title, og:site_name, header/logo, footer, copyright and bounded contact/imprint fragments. It does not score positive identity signals, publish claims or make requests. Existing proof behavior is unchanged until R4 explicitly consumes this veto input.

Hidden/script/template/noscript content, article/news bodies, client/customer/partner/reference sections and logos, and agency credits are excluded. Semantic header/footer tags, ARIA banner/contentinfo and conventional container markers are supported. A contact-page URL does not turn its whole body into publisher context: only small blocks with an address/phone/email/org-number cue qualify. Exact raw page receipts remain the evidence source; normalized fragments are an analysis input, not replacement excerpts.

Seven focused tests cover positive publisher locations/contact, nonsemantic logo/copyright, client lists, partner logos, reference sections, news/article mentions, hidden content, split-node agency credits and inline credit removal while retaining the owner's copyright. The full suite result is recorded in pytest-R1.txt. No new proof tier or positive rule. Remaining limits: text extraction cannot infer CSS-computed visibility or identify every unlabelled third-party section; R4 retains every existing veto as well.
