# P3e scale-500 published website/social inventory

Seed 20261119, 500 companies disjoint from every committed sample, run `r5-p3e-seed20261119-final` from a clean clone. Every published website and social URL is listed with exact saved excerpts, proof tier, retrieval time and SHA-256; each receipt was re-hashed from the saved body and its excerpt found verbatim. Automated verdicts use the existing offline precision-ledger rules (scripts/precision_ledger.py `recheck`); they are rule checks, not human verdicts.

| Kind | Correct | Doubtful | Wrong |
|---|---:|---:|---:|
| website | 22 | 14 | 0 |
| social | 14 | 3 | 5 |

Automated labels are shown exactly as produced. 5 "wrong" label(s) are ledger-tool limitations, not identity findings: `StopIteration` means the legacy recheck found no HTML identity receipt because the site was proven from a linked legal PDF (Stage L2), and "no longer verifies" on `owner_jsonld_sameas_v1` / `own_contact_follow_us_v1` means the legacy social recheck predates the X2 owner-declaration tiers. The full independent verifier (`check_live_run.py`, including `verify_legal_pdf` and `verify_owner_social`) passed every one of them. They stay listed for hand-check below.

## Automated-doubtful or wrong — for hand-check (22)

### 917752591 - NORWEGIAN WOOD DESIGN AS - social

- url: `https://www.facebook.com/Norwegianwooddesign`
- proof tier: `own_header_footer_exact_name_v1`
- automated verdict: **doubtful** (No exact target orgnr in saved owner/proof context; published signal-only tier requires hand review; Published identity tier is below exact-number VERIFIED; Saved page proof needs review: corroboration)

Source: https://norwegianwooddesign.com/

Retrieved: 2026-11-16T17:06:13.503782Z; SHA-256 `b64d785a1992011e8f70d8ae16115f3998064cca3ad23b2873a0b40fc826cbc4`; locator `company-link:https://www.facebook.com/Norwegianwooddesign`; method `signalpost.website.v1`.

<pre>&lt;a href="https://www.facebook.com/Norwegianwooddesign/"&gt;</pre>

Source: https://norwegianwooddesign.com/

Retrieved: 2026-11-16T17:06:13.503782Z; SHA-256 `b64d785a1992011e8f70d8ae16115f3998064cca3ad23b2873a0b40fc826cbc4`; locator `identity-proof:917752591`; method `signalpost.website.v1`.

<pre>title&gt;Unike møbler fra de dype skoger - Norwegian Wood Design&lt;/title&gt;
    &lt;link rel="apple-touch-icon" sizes="180x180" href="https://norwegianwooddesign.com/wp-content/themes/nwd/images/apple-touch-icon.png"&gt;
	&lt;link rel="icon" type="image/png" href="https://norwegianwooddesign.com/wp-content/themes/</pre>

Source: https://norwegianwooddesign.com/

Retrieved: 2026-11-16T17:06:13.503782Z; SHA-256 `b64d785a1992011e8f70d8ae16115f3998064cca3ad23b2873a0b40fc826cbc4`; locator `registry-contact:email_domain`; method `signalpost.registry_contact.v1`.

<pre>&lt;a href="mailto:post@nwdesign.no"&gt;</pre>

### 925792160 - MARINETEAM AS - social

- url: `https://www.facebook.com/MarineteamAS`
- proof tier: `own_header_footer_exact_name_v1`
- automated verdict: **doubtful** (No exact target orgnr in saved owner/proof context; published signal-only tier requires hand review; Published identity tier is below exact-number VERIFIED; Saved page proof needs review: corroboration)

Source: https://marineteam.no/

Retrieved: 2026-11-16T17:05:50.865006Z; SHA-256 `305980f851a4b9f8ac455e7aba42910175e72961042dae9258ecd43151cc9d21`; locator `company-link:https://www.facebook.com/MarineteamAS`; method `signalpost.website.v1`.

<pre>&lt;a href="https://www.facebook.com/MarineteamAS" target="_blank"&gt;</pre>

Source: https://marineteam.no/

Retrieved: 2026-11-16T17:05:50.865006Z; SHA-256 `305980f851a4b9f8ac455e7aba42910175e72961042dae9258ecd43151cc9d21`; locator `identity-proof:925792160`; method `signalpost.website.v1`.

<pre>://marineteam.no/xmlrpc.php"&gt;

		&lt;title&gt;MarineTeam AS&lt;/title&gt;
&lt;meta name='robots' content='max-image-preview:large' /&gt;
&lt;script id="cookie-law-info-gcm-var-js"&gt;
var _ckyGcm = {"status":true,"default_settings":[{"analytics":"denied","advertisement":"denied","functional":"denied","necessary":"granted",</pre>

Source: https://marineteam.no/

Retrieved: 2026-11-16T17:05:50.865006Z; SHA-256 `305980f851a4b9f8ac455e7aba42910175e72961042dae9258ecd43151cc9d21`; locator `registry-contact:email_domain`; method `signalpost.registry_contact.v1`.

<pre>&lt;a href="mailto:post@marineteam.no"&gt;</pre>

Source: https://marineteam.no/

Retrieved: 2026-11-16T17:05:50.865006Z; SHA-256 `305980f851a4b9f8ac455e7aba42910175e72961042dae9258ecd43151cc9d21`; locator `registry-contact:phone`; method `signalpost.registry_contact.v1`.

<pre>nbsp;&lt;/p&gt;
&lt;h4&gt;Kontaktinfo:&lt;/h4&gt;
&lt;p&gt;Tlf: 452 72 700&lt;br /&gt;
E-post: &lt;a href="mailto:post@marineteam.no"&gt;post@marineteam.no&lt;/a&gt;&lt;/p&gt;
	
			&lt;/div&gt;
		&lt;/div&gt;

	&lt;/div&gt;
&lt;/div&gt;

&lt;div id="forstickbottomto"&gt;&lt;/div&gt; &lt;div id="map"&gt;&lt;/div&gt;
    &lt;script&gt;
      function initMap() {
        // Styles a map in night mode.
</pre>

### 925792160 - MARINETEAM AS - social

- url: `https://www.instagram.com/marineteamas`
- proof tier: `own_header_footer_exact_name_v1`
- automated verdict: **doubtful** (No exact target orgnr in saved owner/proof context; published signal-only tier requires hand review; Published identity tier is below exact-number VERIFIED; Saved page proof needs review: corroboration)

Source: https://marineteam.no/

Retrieved: 2026-11-16T17:05:50.865006Z; SHA-256 `305980f851a4b9f8ac455e7aba42910175e72961042dae9258ecd43151cc9d21`; locator `company-link:https://www.instagram.com/marineteamas`; method `signalpost.website.v1`.

<pre>&lt;a href="https://www.instagram.com/marineteamas/" target="_blank"&gt;</pre>

Source: https://marineteam.no/

Retrieved: 2026-11-16T17:05:50.865006Z; SHA-256 `305980f851a4b9f8ac455e7aba42910175e72961042dae9258ecd43151cc9d21`; locator `identity-proof:925792160`; method `signalpost.website.v1`.

<pre>://marineteam.no/xmlrpc.php"&gt;

		&lt;title&gt;MarineTeam AS&lt;/title&gt;
&lt;meta name='robots' content='max-image-preview:large' /&gt;
&lt;script id="cookie-law-info-gcm-var-js"&gt;
var _ckyGcm = {"status":true,"default_settings":[{"analytics":"denied","advertisement":"denied","functional":"denied","necessary":"granted",</pre>

Source: https://marineteam.no/

Retrieved: 2026-11-16T17:05:50.865006Z; SHA-256 `305980f851a4b9f8ac455e7aba42910175e72961042dae9258ecd43151cc9d21`; locator `registry-contact:email_domain`; method `signalpost.registry_contact.v1`.

<pre>&lt;a href="mailto:post@marineteam.no"&gt;</pre>

Source: https://marineteam.no/

Retrieved: 2026-11-16T17:05:50.865006Z; SHA-256 `305980f851a4b9f8ac455e7aba42910175e72961042dae9258ecd43151cc9d21`; locator `registry-contact:phone`; method `signalpost.registry_contact.v1`.

<pre>nbsp;&lt;/p&gt;
&lt;h4&gt;Kontaktinfo:&lt;/h4&gt;
&lt;p&gt;Tlf: 452 72 700&lt;br /&gt;
E-post: &lt;a href="mailto:post@marineteam.no"&gt;post@marineteam.no&lt;/a&gt;&lt;/p&gt;
	
			&lt;/div&gt;
		&lt;/div&gt;

	&lt;/div&gt;
&lt;/div&gt;

&lt;div id="forstickbottomto"&gt;&lt;/div&gt; &lt;div id="map"&gt;&lt;/div&gt;
    &lt;script&gt;
      function initMap() {
        // Styles a map in night mode.
</pre>

### 927612372 - CONTUR AS - social

- url: `https://no.linkedin.com/company/contur2023`
- proof tier: `own_contact_follow_us_v1`
- automated verdict: **wrong** (own header/footer/name/numeric-link policy no longer verifies)

Source: https://contur.no/kontakt/

Retrieved: 2026-11-16T17:07:03.487240Z; SHA-256 `18828a0f965f29c11e98bfe2794ffd30fb030df2e090df869301e88a4fd70d1a`; locator `company-link:https://no.linkedin.com/company/contur2023`; method `signalpost.website.v1`.

<pre>&lt;a href="https://no.linkedin.com/company/contur2023" class="group"&gt;</pre>

Source: https://contur.no/kontakt/

Retrieved: 2026-11-16T17:07:03.487240Z; SHA-256 `18828a0f965f29c11e98bfe2794ffd30fb030df2e090df869301e88a4fd70d1a`; locator `identity-proof:927612372`; method `signalpost.website.v1`.

<pre>ich-text"&gt;&lt;h3&gt;Contur AS&lt;/h3&gt;
&lt;p&gt;Org.nr. 927 612 372&lt;/p&gt;
&lt;p&gt;&lt;strong&gt;Adresse:&lt;/strong&gt;&lt;br /&gt;
Vige Havnevei 4, 4. etg.&lt;br /&gt;
4633 Kristiansand&lt;/p&gt;
&lt;p&gt;Tel</pre>

### 927612372 - CONTUR AS - social

- url: `https://www.facebook.com/contur2023`
- proof tier: `own_contact_follow_us_v1`
- automated verdict: **wrong** (own header/footer/name/numeric-link policy no longer verifies)

Source: https://contur.no/kontakt/

Retrieved: 2026-11-16T17:07:03.487240Z; SHA-256 `18828a0f965f29c11e98bfe2794ffd30fb030df2e090df869301e88a4fd70d1a`; locator `company-link:https://www.facebook.com/contur2023`; method `signalpost.website.v1`.

<pre>&lt;a href="https://www.facebook.com/contur2023/?locale=nb_NO" class="group"&gt;</pre>

Source: https://contur.no/kontakt/

Retrieved: 2026-11-16T17:07:03.487240Z; SHA-256 `18828a0f965f29c11e98bfe2794ffd30fb030df2e090df869301e88a4fd70d1a`; locator `identity-proof:927612372`; method `signalpost.website.v1`.

<pre>ich-text"&gt;&lt;h3&gt;Contur AS&lt;/h3&gt;
&lt;p&gt;Org.nr. 927 612 372&lt;/p&gt;
&lt;p&gt;&lt;strong&gt;Adresse:&lt;/strong&gt;&lt;br /&gt;
Vige Havnevei 4, 4. etg.&lt;br /&gt;
4633 Kristiansand&lt;/p&gt;
&lt;p&gt;Tel</pre>

### 970545204 - MISJONSKIRKEN UNG - social

- url: `https://www.facebook.com/MisjonskirkenUNG`
- proof tier: `owner_jsonld_sameas_v1`
- automated verdict: **wrong** (own header/footer/name/numeric-link policy no longer verifies)

Source: https://www.mkung.no/

Retrieved: 2026-11-16T17:04:57.464216Z; SHA-256 `a451b6c03c8f7171401c9bbdb9d2fc0174a966bef27d30b208ad74d8ceba9873`; locator `company-link:https://www.facebook.com/MisjonskirkenUNG`; method `signalpost.website.v1`.

<pre>tps:\/\/www.mkung.no\/#\/schema\/logo\/image\/"},"sameAs":["https:\/\/www.facebook.com\/MisjonskirkenUNG\/","https:\/\/www.instagram.com\/misjonskirkenung\/","https:\</pre>

Source: https://www.mkung.no/

Retrieved: 2026-11-16T17:04:57.464216Z; SHA-256 `a451b6c03c8f7171401c9bbdb9d2fc0174a966bef27d30b208ad74d8ceba9873`; locator `identity-proof:970545204`; method `signalpost.website.v1`.

<pre>yoast-seo-wordpress/ --&gt;
	&lt;title&gt;Hjem - Misjonskirken UNG&lt;/title&gt;
	&lt;link rel="canonical" href="https://www.mkung.no/" /&gt;
	&lt;meta property="og:locale" content="nb_NO" /&gt;
	&lt;meta property="og:type" content="website" /&gt;
	&lt;meta property="og:title" content="Hjem - Misjonskirken UNG" /&gt;
	&lt;meta property="og:</pre>

Source: https://www.mkung.no/

Retrieved: 2026-11-16T17:04:57.464216Z; SHA-256 `a451b6c03c8f7171401c9bbdb9d2fc0174a966bef27d30b208ad74d8ceba9873`; locator `registry-contact:email_domain`; method `signalpost.registry_contact.v1`.

<pre>&lt;a href="mailto:ung@mknu.no"&gt;</pre>

### 970545204 - MISJONSKIRKEN UNG - social

- url: `https://www.instagram.com/misjonskirkenung`
- proof tier: `owner_jsonld_sameas_v1`
- automated verdict: **wrong** (own header/footer/name/numeric-link policy no longer verifies)

Source: https://www.mkung.no/

Retrieved: 2026-11-16T17:04:57.464216Z; SHA-256 `a451b6c03c8f7171401c9bbdb9d2fc0174a966bef27d30b208ad74d8ceba9873`; locator `company-link:https://www.instagram.com/misjonskirkenung`; method `signalpost.website.v1`.

<pre>"sameAs":["https:\/\/www.facebook.com\/MisjonskirkenUNG\/","https:\/\/www.instagram.com\/misjonskirkenung\/","https:\/\/www.youtube.com\/channel\/UCkCcNuvONObRzz70pa58</pre>

Source: https://www.mkung.no/

Retrieved: 2026-11-16T17:04:57.464216Z; SHA-256 `a451b6c03c8f7171401c9bbdb9d2fc0174a966bef27d30b208ad74d8ceba9873`; locator `identity-proof:970545204`; method `signalpost.website.v1`.

<pre>yoast-seo-wordpress/ --&gt;
	&lt;title&gt;Hjem - Misjonskirken UNG&lt;/title&gt;
	&lt;link rel="canonical" href="https://www.mkung.no/" /&gt;
	&lt;meta property="og:locale" content="nb_NO" /&gt;
	&lt;meta property="og:type" content="website" /&gt;
	&lt;meta property="og:title" content="Hjem - Misjonskirken UNG" /&gt;
	&lt;meta property="og:</pre>

Source: https://www.mkung.no/

Retrieved: 2026-11-16T17:04:57.464216Z; SHA-256 `a451b6c03c8f7171401c9bbdb9d2fc0174a966bef27d30b208ad74d8ceba9873`; locator `registry-contact:email_domain`; method `signalpost.registry_contact.v1`.

<pre>&lt;a href="mailto:ung@mknu.no"&gt;</pre>

### 970545204 - MISJONSKIRKEN UNG - social

- url: `https://www.youtube.com/channel/UCkCcNuvONObRzz70pa5855A`
- proof tier: `owner_jsonld_sameas_v1`
- automated verdict: **wrong** (own header/footer/name/numeric-link policy no longer verifies)

Source: https://www.mkung.no/

Retrieved: 2026-11-16T17:04:57.464216Z; SHA-256 `a451b6c03c8f7171401c9bbdb9d2fc0174a966bef27d30b208ad74d8ceba9873`; locator `company-link:https://www.youtube.com/channel/UCkCcNuvONObRzz70pa5855A`; method `signalpost.website.v1`.

<pre>enUNG\/","https:\/\/www.instagram.com\/misjonskirkenung\/","https:\/\/www.youtube.com\/channel\/UCkCcNuvONObRzz70pa5855A"]}]}</pre>

Source: https://www.mkung.no/

Retrieved: 2026-11-16T17:04:57.464216Z; SHA-256 `a451b6c03c8f7171401c9bbdb9d2fc0174a966bef27d30b208ad74d8ceba9873`; locator `identity-proof:970545204`; method `signalpost.website.v1`.

<pre>yoast-seo-wordpress/ --&gt;
	&lt;title&gt;Hjem - Misjonskirken UNG&lt;/title&gt;
	&lt;link rel="canonical" href="https://www.mkung.no/" /&gt;
	&lt;meta property="og:locale" content="nb_NO" /&gt;
	&lt;meta property="og:type" content="website" /&gt;
	&lt;meta property="og:title" content="Hjem - Misjonskirken UNG" /&gt;
	&lt;meta property="og:</pre>

Source: https://www.mkung.no/

Retrieved: 2026-11-16T17:04:57.464216Z; SHA-256 `a451b6c03c8f7171401c9bbdb9d2fc0174a966bef27d30b208ad74d8ceba9873`; locator `registry-contact:email_domain`; method `signalpost.registry_contact.v1`.

<pre>&lt;a href="mailto:ung@mknu.no"&gt;</pre>

### 820546342 - ROYAL CLOUD SOLUTIONS - website

- url: `https://www.royalcloudsolutions.no`
- proof tier: `registry_declared_publisher_name`
- identity level: `HIGH`
- automated verdict: **doubtful** (No exact target orgnr in saved owner/proof context; published signal-only tier requires hand review; Published identity tier is below exact-number VERIFIED; Saved page proof needs review: corroboration)

Source: https://www.royalcloudsolutions.no/

Retrieved: 2026-11-16T17:04:02.907125Z; SHA-256 `18ce964e9d38664a9bf03165f6a3a21d553499745380acba011c728063593e8e`; locator `identity-proof:820546342`; method `signalpost.website.v1`.

<pre>lcloudsolutions.no/xmlrpc.php"&gt;

&lt;title&gt;Royal Cloud Solutions &amp;#8211; Electronics and smart software&lt;/title&gt;
&lt;meta name='robots' content='max-image-preview:large' /&gt;
&lt;link rel="alternate" type="application/rss+xml" title="Royal Cloud Solutions &amp;raquo; Feed" href="https://www.royalcloudsolutions.no/f</pre>

### 916907354 - HELSESMART.NO AS - website

- url: `https://helsesmart.no`
- proof tier: `orgnr_on_page`
- identity level: `VERIFIED`
- automated verdict: **doubtful** (Exact registry legal/brand spelling not located in saved page text)

Source: https://helsesmart.no/

Retrieved: 2026-11-16T17:05:59.510984Z; SHA-256 `74f1f70943682de6141ae83731f6b1874a977e2181fa1680f895c948a59446b1`; locator `identity-proof:916907354`; method `signalpost.website.v1`.

<pre>orgnr=916907354" rel="nofollow"&gt;Org.nr. 916 907 354&lt;/a&gt;&lt;/span&gt;
            &lt;span&gt;&lt;a href="/hjelp/retningslinjer/personvern"&gt;Personvern&lt;/a&gt; · &lt;a href="</pre>

### 917752591 - NORWEGIAN WOOD DESIGN AS - website

- url: `https://norwegianwooddesign.com`
- proof tier: `registry_declared_live`
- identity level: `HIGH`
- automated verdict: **doubtful** (No exact target orgnr in saved owner/proof context; published signal-only tier requires hand review; Published identity tier is below exact-number VERIFIED; Saved page proof needs review: corroboration)

Source: https://norwegianwooddesign.com/

Retrieved: 2026-11-16T17:06:13.503782Z; SHA-256 `b64d785a1992011e8f70d8ae16115f3998064cca3ad23b2873a0b40fc826cbc4`; locator `identity-proof:917752591`; method `signalpost.website.v1`.

<pre>title&gt;Unike møbler fra de dype skoger - Norwegian Wood Design&lt;/title&gt;
    &lt;link rel="apple-touch-icon" sizes="180x180" href="https://norwegianwooddesign.com/wp-content/themes/nwd/images/apple-touch-icon.png"&gt;
	&lt;link rel="icon" type="image/png" href="https://norwegianwooddesign.com/wp-content/themes/</pre>

Source: https://norwegianwooddesign.com/

Retrieved: 2026-11-16T17:06:13.503782Z; SHA-256 `b64d785a1992011e8f70d8ae16115f3998064cca3ad23b2873a0b40fc826cbc4`; locator `registry-contact:email_domain`; method `signalpost.registry_contact.v1`.

<pre>&lt;a href="mailto:post@nwdesign.no"&gt;</pre>

### 925769371 - ALFA DEKK AS - website

- url: `https://www.alfadekk.no`
- proof tier: `publisher_name_registered_place`
- identity level: `HIGH`
- automated verdict: **doubtful** (No exact target orgnr in saved owner/proof context; published signal-only tier requires hand review; Published identity tier is below exact-number VERIFIED; Saved page proof needs review: corroboration)

Source: https://www.alfadekk.no/

Retrieved: 2026-11-16T17:07:13.316771Z; SHA-256 `b4fc29c409998dd572fe4a8e9938a828659d2a146ce499c4a91c3820ff3a66cf`; locator `identity-proof:925769371`; method `signalpost.website.v1`.

<pre>AFAFA;" class="wixui-rich-text__text"&gt;&amp;copy; Alfa Dekk AS // &lt;a href="https://www.alfadekk.no/personvern" target="_self" class="wixui-rich-text__text"&gt;Personvern&lt;/a&gt;&lt;/span&gt;&lt;/p&gt;&lt;/div&gt;&lt;!--/$--&gt;&lt;/div&gt;&lt;/div&gt;&lt;/div&gt;&lt;!--/$--&gt;&lt;!--$--&gt;&lt;div id="comp-libsnmgg" class="comp-libsnmgg FDI5TK wixui-column-strip__co</pre>

### 925792160 - MARINETEAM AS - website

- url: `https://marineteam.no`
- proof tier: `signals`
- identity level: `HIGH`
- automated verdict: **doubtful** (No exact target orgnr in saved owner/proof context; published signal-only tier requires hand review; Published identity tier is below exact-number VERIFIED; Saved page proof needs review: corroboration)

Source: https://marineteam.no/

Retrieved: 2026-11-16T17:05:50.865006Z; SHA-256 `305980f851a4b9f8ac455e7aba42910175e72961042dae9258ecd43151cc9d21`; locator `identity-proof:925792160`; method `signalpost.website.v1`.

<pre>://marineteam.no/xmlrpc.php"&gt;

		&lt;title&gt;MarineTeam AS&lt;/title&gt;
&lt;meta name='robots' content='max-image-preview:large' /&gt;
&lt;script id="cookie-law-info-gcm-var-js"&gt;
var _ckyGcm = {"status":true,"default_settings":[{"analytics":"denied","advertisement":"denied","functional":"denied","necessary":"granted",</pre>

Source: https://marineteam.no/

Retrieved: 2026-11-16T17:05:50.865006Z; SHA-256 `305980f851a4b9f8ac455e7aba42910175e72961042dae9258ecd43151cc9d21`; locator `registry-contact:email_domain`; method `signalpost.registry_contact.v1`.

<pre>&lt;a href="mailto:post@marineteam.no"&gt;</pre>

Source: https://marineteam.no/

Retrieved: 2026-11-16T17:05:50.865006Z; SHA-256 `305980f851a4b9f8ac455e7aba42910175e72961042dae9258ecd43151cc9d21`; locator `registry-contact:phone`; method `signalpost.registry_contact.v1`.

<pre>nbsp;&lt;/p&gt;
&lt;h4&gt;Kontaktinfo:&lt;/h4&gt;
&lt;p&gt;Tlf: 452 72 700&lt;br /&gt;
E-post: &lt;a href="mailto:post@marineteam.no"&gt;post@marineteam.no&lt;/a&gt;&lt;/p&gt;
	
			&lt;/div&gt;
		&lt;/div&gt;

	&lt;/div&gt;
&lt;/div&gt;

&lt;div id="forstickbottomto"&gt;&lt;/div&gt; &lt;div id="map"&gt;&lt;/div&gt;
    &lt;script&gt;
      function initMap() {
        // Styles a map in night mode.
</pre>

### 928066274 - RØYR DENTAL AS - website

- url: `https://www.royrdental.no`
- proof tier: `publisher_name_registered_place`
- identity level: `HIGH`
- automated verdict: **doubtful** (No exact target orgnr in saved owner/proof context; published signal-only tier requires hand review; Published identity tier is below exact-number VERIFIED; Saved page proof needs review: corroboration)

Source: https://www.royrdental.no/

Retrieved: 2026-11-16T17:04:40.621626Z; SHA-256 `96c7a5f66cf63918e478dc3124ed0379d2e98ca4617048f0fc5f5751f08257ff`; locator `identity-proof:928066274`; method `signalpost.website.v1`.

<pre>7c4fec5182.css" rel="stylesheet"&gt;&lt;title&gt;Røyr Dental AS | Autorisert tannteknisk laboratorium&lt;/title&gt;&lt;meta name='robots' content='max-image-preview:large' /&gt;&lt;link rel="alternate" title="oEmbed (JSON)" type="application/json+oembed" href="https://www.royrdental.no/wp-json/oembed/1.0/embed?url=https%3A</pre>

### 954825736 - KONGSVINGER BOLIGSTIFTELSE - website

- url: `https://boligstiftelse.no`
- proof tier: `signals`
- identity level: `HIGH`
- automated verdict: **doubtful** (No exact target orgnr in saved owner/proof context; published signal-only tier requires hand review; Published identity tier is below exact-number VERIFIED; Saved page proof needs review: corroboration)

Source: https://boligstiftelse.no/

Retrieved: 2026-11-16T17:04:45.846797Z; SHA-256 `cfc33dc1a542c432b5e28c7759a111144b1307150824e0f34a6cc4e24cb387ef`; locator `identity-proof:954825736`; method `signalpost.website.v1`.

<pre> PRO - https://rankmath.com/ --&gt;
&lt;title&gt;Kongsvinger Boligstiftelse&lt;/title&gt;
&lt;meta name="description" content="Kongsvinger Boligstiftelse er en virksomhet som hjelper vanskligstilte, for eksempel eldre eller de med psykisk utviklingshemming, med leie av bolig"/&gt;
&lt;meta name="robots" content="follow, in</pre>

Source: https://boligstiftelse.no/

Retrieved: 2026-11-16T17:04:45.846797Z; SHA-256 `cfc33dc1a542c432b5e28c7759a111144b1307150824e0f34a6cc4e24cb387ef`; locator `registry-contact:phone`; method `signalpost.registry_contact.v1`.

<pre>&lt;a href="tel:004762817573"&gt;</pre>

### 959835047 - KEYBACK NØKKELBRIKKER AS - website

- url: `https://keyback.no`
- proof tier: `registry_declared_publisher_name`
- identity level: `HIGH`
- automated verdict: **doubtful** (No exact target orgnr in saved owner/proof context; published signal-only tier requires hand review; Published identity tier is below exact-number VERIFIED; Saved page proof needs review: corroboration)

Source: https://keyback.no/

Retrieved: 2026-11-16T17:06:39.748118Z; SHA-256 `15a77392ebfd4aac8e083b97eee826f78ae3b088ff8b6eae4ec6be703dedd92e`; locator `identity-proof:959835047`; method `signalpost.website.v1`.

<pre>te-info"&gt;
		&lt;div class="footer-text"&gt;
		Keyback Nøkkelbrikker AS - P.b. 5373 Majorstuen - 0304 - Oslo - Tel: 810 33 010 - E-post: &lt;a href="mailto:service@keyback.no?Subject=Melding%20til%20Keyback"&gt;service@keyback.no&lt;/a&gt;	&lt;/div&gt;
	
	&lt;/div&gt;

			&lt;/div&gt;
&lt;/footer&gt;		&lt;/div&gt;

		&lt;script type="text/javascript"</pre>

Source: https://keyback.no/

Retrieved: 2026-11-16T17:06:39.748118Z; SHA-256 `15a77392ebfd4aac8e083b97eee826f78ae3b088ff8b6eae4ec6be703dedd92e`; locator `registry-contact:email_domain`; method `signalpost.registry_contact.v1`.

<pre>&lt;a href="mailto:service@keyback.no?Subject=Melding%20til%20Keyback"&gt;</pre>

### 966097892 - VORMSUND BARNEHAGE SA - website

- url: `https://vormsund.barnehage.no`
- proof tier: `signals`
- identity level: `HIGH`
- automated verdict: **doubtful** (No exact target orgnr in saved owner/proof context; published signal-only tier requires hand review; Published identity tier is below exact-number VERIFIED; Saved page proof needs review: corroboration)

Source: https://vormsund.barnehage.no/

Retrieved: 2026-11-16T17:03:49.108021Z; SHA-256 `c7d87ee4ddec086c727dca1076294f8cfba6fc95f54ef90342809306172b3a33`; locator `identity-proof:966097892`; method `signalpost.website.v1`.

<pre>lesheet" type="text/css" /&gt;
    &lt;title&gt;Vormsund barnehage SA&lt;/title&gt;
    &lt;script src="/Scripts/jquery-1.8.3.min.js" type="text/javascript"&gt;&lt;/script&gt;
    &lt;script src="/Scripts/jquery.unobtrusive-ajax.min.js" type="text/javascript"&gt;&lt;/script&gt;
    &lt;script src="/Scripts/modernizr-1.7.min.js" type="te</pre>

Source: https://vormsund.barnehage.no/

Retrieved: 2026-11-16T17:03:49.108021Z; SHA-256 `c7d87ee4ddec086c727dca1076294f8cfba6fc95f54ef90342809306172b3a33`; locator `registry-contact:email_domain`; method `signalpost.registry_contact.v1`.

<pre>&lt;a href="mailto:Wenche@vormsundbhg.no"&gt;</pre>

### 970545204 - MISJONSKIRKEN UNG - website

- url: `https://www.mkung.no`
- proof tier: `registry_declared_publisher_name`
- identity level: `HIGH`
- automated verdict: **doubtful** (No exact target orgnr in saved owner/proof context; published signal-only tier requires hand review; Published identity tier is below exact-number VERIFIED; Saved page proof needs review: corroboration)

Source: https://www.mkung.no/

Retrieved: 2026-11-16T17:04:57.464216Z; SHA-256 `a451b6c03c8f7171401c9bbdb9d2fc0174a966bef27d30b208ad74d8ceba9873`; locator `identity-proof:970545204`; method `signalpost.website.v1`.

<pre>yoast-seo-wordpress/ --&gt;
	&lt;title&gt;Hjem - Misjonskirken UNG&lt;/title&gt;
	&lt;link rel="canonical" href="https://www.mkung.no/" /&gt;
	&lt;meta property="og:locale" content="nb_NO" /&gt;
	&lt;meta property="og:type" content="website" /&gt;
	&lt;meta property="og:title" content="Hjem - Misjonskirken UNG" /&gt;
	&lt;meta property="og:</pre>

Source: https://www.mkung.no/

Retrieved: 2026-11-16T17:04:57.464216Z; SHA-256 `a451b6c03c8f7171401c9bbdb9d2fc0174a966bef27d30b208ad74d8ceba9873`; locator `registry-contact:email_domain`; method `signalpost.registry_contact.v1`.

<pre>&lt;a href="mailto:ung@mknu.no"&gt;</pre>

### 974683520 - MEDITEAM AS - website

- url: `https://www.mediteam.no`
- proof tier: `signals`
- identity level: `HIGH`
- automated verdict: **doubtful** (No exact target orgnr in saved owner/proof context; published signal-only tier requires hand review; Published identity tier is below exact-number VERIFIED; Saved page proof needs review: corroboration)

Source: https://www.mediteam.no/

Retrieved: 2026-11-16T17:05:38.823855Z; SHA-256 `2c3c81c3ee9fb561ceb38772e81f4202b47fe8555f353b8cacd97ec349e71a91`; locator `identity-proof:974683520`; method `signalpost.website.v1`.

<pre>ref=""&gt;
&lt;meta charset="utf-8" /&gt;
&lt;title&gt;Mediteam | Enhance Work Safety Today&lt;/title&gt;
&lt;meta http-equiv="Accept-CH" content="Sec-CH-UA-Platform-Version, Sec-CH-UA-Model" /&gt;&lt;link rel="icon" type="image/x-icon" href="https://assets.squarespace.com/universal/default-favicon.ico"/&gt;
&lt;link rel="canonical" h</pre>

Source: https://www.mediteam.no/

Retrieved: 2026-11-16T17:05:38.823855Z; SHA-256 `2c3c81c3ee9fb561ceb38772e81f4202b47fe8555f353b8cacd97ec349e71a91`; locator `registry-contact:email_domain`; method `signalpost.registry_contact.v1`.

<pre>&lt;a href="mailto:john.hjelle@mediteam.no?" target="_blank"&gt;</pre>

Source: https://www.mediteam.no/

Retrieved: 2026-11-16T17:05:38.823855Z; SHA-256 `2c3c81c3ee9fb561ceb38772e81f4202b47fe8555f353b8cacd97ec349e71a91`; locator `registry-contact:phone`; method `signalpost.registry_contact.v1`.

<pre>&lt;a href="tel:+4751856100" target="_blank"&gt;</pre>

### 978656633 - ENGERDAL ELEKTRO AS - website

- url: `https://engerdal-elektro.no`
- proof tier: `registry_declared_publisher_name`
- identity level: `HIGH`
- automated verdict: **doubtful** (No exact target orgnr in saved owner/proof context; published signal-only tier requires hand review; Published identity tier is below exact-number VERIFIED; Saved page proof needs review: corroboration)

Source: https://engerdal-elektro.no/

Retrieved: 2026-11-16T17:04:08.705794Z; SHA-256 `b0263ba69b331c1c92fac4e1be451150f9fdb84031c7d3e9a3f467f757e61cba`; locator `identity-proof:978656633`; method `signalpost.website.v1`.

<pre>ight"&gt;© Alle Rettigheter er Reservert | Engerdal Elektro AS&lt;/div&gt;&lt;div class="footer-rights-wrapper"&gt;&lt;div class="w-embed"&gt;&lt;uab-badge theme="dark" align="right"&gt;&lt;/uab-badge&gt;&lt;/div&gt;&lt;/div&gt;&lt;/div&gt;&lt;/div&gt;&lt;/div&gt;&lt;script src="https://d3e54v103j8qbb.cloudfront.net/js/jquery-3.5.1.min.dc5e7f18c8.js?site=686aebf9c</pre>

Source: https://engerdal-elektro.no/

Retrieved: 2026-11-16T17:04:08.705794Z; SHA-256 `b0263ba69b331c1c92fac4e1be451150f9fdb84031c7d3e9a3f467f757e61cba`; locator `registry-contact:email_domain`; method `signalpost.registry_contact.v1`.

<pre>&lt;a href="mailto:post@engerdal-elektro.no" class="form-link"&gt;</pre>

Source: https://engerdal-elektro.no/

Retrieved: 2026-11-16T17:04:08.705794Z; SHA-256 `b0263ba69b331c1c92fac4e1be451150f9fdb84031c7d3e9a3f467f757e61cba`; locator `registry-contact:phone`; method `signalpost.registry_contact.v1`.

<pre>&lt;a href="tel:+4762458290" class="footer-links"&gt;</pre>

### 994968181 - STRØMBERG ELEKTRO AS - website

- url: `https://www.strombergelektro.no`
- proof tier: `signals`
- identity level: `HIGH`
- automated verdict: **doubtful** (No exact target orgnr in saved owner/proof context; published signal-only tier requires hand review; Published identity tier is below exact-number VERIFIED; Saved page proof needs review: corroboration)

Source: https://www.strombergelektro.no/

Retrieved: 2026-11-16T17:05:22.567378Z; SHA-256 `5b55d998930c8495bf10888763df9944f03c0cff0c35523b8f3958020a72c17b`; locator `identity-proof:994968181`; method `signalpost.website.v1`.

<pre>ntent="text/html; charset=utf-8"&gt;&lt;title&gt;Strømberg Elektro as - OM OSS&lt;/title&gt;&lt;meta name="DESCRIPTION" content=""&gt;&lt;meta name="KEYWORDS" content=""&gt;&lt;meta name="GENERATOR" content="Parallels Plesk Sitebuilder 4.5.0"&gt;&lt;link href="css/styles.css?template=vap-29&amp;colorScheme=black&amp;header=&amp;button=buttons1" r</pre>

Source: https://www.strombergelektro.no/

Retrieved: 2026-11-16T17:05:22.567378Z; SHA-256 `5b55d998930c8495bf10888763df9944f03c0cff0c35523b8f3958020a72c17b`; locator `registry-contact:email_domain`; method `signalpost.registry_contact.v1`.

<pre>opyright"&gt;Telefon 91 00 36 20 • e-post: magne@strombergelektro.no • www.strombergelektro.no&lt;/td&gt;&lt;/tr&gt;&lt;/table&gt;&lt;/td&gt;&lt;/tr&gt;&lt;/table&gt;&lt;/td&gt;&lt;/tr&gt;&lt;/table&gt;&lt;/center&gt;&lt;/body&gt;&lt;/html&gt;
</pre>

### 995053225 - STARO TECH AS - website

- url: `https://www.staro.no`
- proof tier: `registry_declared_publisher_name`
- identity level: `HIGH`
- automated verdict: **doubtful** (No exact target orgnr in saved owner/proof context; published signal-only tier requires hand review; Published identity tier is below exact-number VERIFIED; Saved page proof needs review: corroboration)

Source: https://www.staro.no/

Retrieved: 2026-11-16T17:04:04.779771Z; SHA-256 `93508edce9e475f5f988e0d32deb8a59fd0cb0edbb05fa18574ad754188c944a`; locator `identity-proof:995053225`; method `signalpost.website.v1`.

<pre>ef="https://gmpg.org/xfn/11"&gt;

&lt;title&gt;Staro Tech AS &amp;#8211; &amp;#8211; Din  samarbeidspartner innen mekanikk, hydraulikk og maskinering&lt;/title&gt;
&lt;meta name='robots' content='max-image-preview:large' /&gt;
&lt;link rel='dns-prefetch' href='//fonts.googleapis.com' /&gt;
&lt;link rel="alternate" type="application/rs</pre>

## Website — automated correct (22)

### 813587912 - FUSA LYD & LYS AS - website

- url: `https://www.fusalydlys.no`
- proof tier: `orgnr_on_page`
- identity level: `VERIFIED`
- automated verdict: **correct**

Source: https://www.fusalydlys.no/

Retrieved: 2026-11-16T17:41:27.422493Z; SHA-256 `69dd14e12b094efac98eedc487a69c88043099c639d376f99763038be2fffc04`; locator `identity-proof:813587912`; method `signalpost.website.v1`.

<pre> 97 71 16 87 / 92 67 05 48&lt;/p&gt;&lt;p&gt;Org.nr 813 587 912&lt;/p&gt;
&lt;/div&gt;
&lt;/div&gt;&lt;/div&gt;
&lt;/div&gt;&lt;div class="c cf" style="width:19.139%;"&gt;
	&lt;div class="c-c cf"&gt;&lt;d</pre>

### 828451162 - SJ SOL AS - website

- url: `https://www.sjsol.no`
- proof tier: `jsonld_vatid`
- identity level: `VERIFIED`
- automated verdict: **correct**

Source: https://www.sjsol.no/

Retrieved: 2026-11-16T17:04:37.399372Z; SHA-256 `859e23ea457932d3114762a524360f2c58f8c5ae5b029cd2adfa16a427da74e5`; locator `identity-proof:828451162`; method `signalpost.website.v1`.

<pre>a-astro-cid-jo6i4kqk&gt;SJ SOL AS, org.nr. 828 451 162&lt;/span&gt;
    &lt;span data-astro-cid-jo6i4kqk&gt;© 2026 SJ SOL AS&lt;/span&gt;
  &lt;/div&gt;
&lt;/footer&gt;
  &lt;/body&gt;
&lt;/ht</pre>

### 891602502 - SNERTINGDAL BYGG & GRAVESERVICE AS - website

- url: `https://snertbygg.no`
- proof tier: `orgnr_on_page`
- identity level: `VERIFIED`
- automated verdict: **correct**

Source: https://snertbygg.no/

Retrieved: 2026-11-16T17:05:57.082412Z; SHA-256 `b0c5486f819f904c28f5dcd60e4ec74c2c085c4e968e3848b7349d36b63d4d10`; locator `identity-proof:891602502`; method `signalpost.website.v1`.

<pre>&lt;/h2&gt;&lt;p data-astro-cid-jo6i4kqk&gt;Org.nr. 891 602 502&lt;/p&gt;&lt;address data-astro-cid-jo6i4kqk&gt;&lt;a href="https://www.google.com/maps/place/Snertingdal+Bygg+%2</pre>

### 897198452 - VERDIHUSET AS - website

- url: `https://www.verdihuset.no`
- proof tier: `orgnr_on_page`
- identity level: `VERIFIED`
- automated verdict: **correct**

Source: https://www.verdihuset.no/

Retrieved: 2026-11-16T17:04:47.356120Z; SHA-256 `24215c66b315bfab23146ee68ce450c7212071dafc3af243b13c3647c461d6a9`; locator `identity-proof:897198452`; method `signalpost.website.v1`.

<pre>ey="paragraph"&gt;
            &lt;p&gt;Org. nr: 897198452&lt;/p&gt;&lt;p&gt;Adresse:&lt;br&gt;Ski: Bråtenveien 3, 1423 Ski&lt;br&gt;Bergen: Storetveitvegen 22, 5067 Bergen&lt;/p&gt;&lt;p&gt;E-po</pre>

Source: https://www.verdihuset.no/

Retrieved: 2026-11-16T17:04:47.356120Z; SHA-256 `24215c66b315bfab23146ee68ce450c7212071dafc3af243b13c3647c461d6a9`; locator `registry-contact:phone`; method `signalpost.registry_contact.v1`.

<pre>er06.01.265.jpg",
        "telephone": "410 88 888",
        "contactPoint": {
            "@type": "ContactPoint",
            "telephone": "410 88 888",
            "contactType": "NO",
            "areaServed": "NO",
            "availableLanguage": "no",
            "url": "https://www.verdihuse</pre>

### 912154602 - FASK-TOOLS AS - website

- url: `https://www.fask-tools.com`
- proof tier: `orgnr_on_page`
- identity level: `VERIFIED`
- automated verdict: **correct**

Source: https://www.fask-tools.com/

Retrieved: 2026-11-16T17:07:15.090021Z; SHA-256 `450c99061a3ab030b09d72130a913676ea9fe9abee5d33d0046b23f24f1537b8`; locator `identity-proof:912154602`; method `signalpost.website.v1`.

<pre>class="font-tit fw-semibold fs-20"&gt;CRN: 912 154 602&lt;/div&gt;&lt;/div&gt;
&lt;div class="col-lg-3 col-sm-6 col-12"&gt;&lt;div class="d-flex mb-10 align-items-center wp-e</pre>

### 916009208 - LINDIT AS - website

- url: `https://www.lindit.no`
- proof tier: `orgnr_on_page`
- identity level: `VERIFIED`
- automated verdict: **correct**

Source: https://www.lindit.no/

Retrieved: 2026-11-16T17:06:04.513049Z; SHA-256 `1d739ffa138cb6e1c6ebfaec5a85bbd6a24cf5bedfbe197f76190a0b8fed59a2`; locator `identity-proof:916009208`; method `signalpost.website.v1`.

<pre>dy-P"&gt;&lt;span class="Normal2-C0"&gt;Org.nr.NO916009208MVA -&lt;wbr&gt; Tlf: 96010899 -&lt;wbr&gt; kontakt@lindit.no&lt;/span&gt;&lt;/p&gt;
&lt;p class="Artistic-Body-P"&gt;&lt;span class="</pre>

### 917571163 - SANTOSHA AS - website

- url: `https://www.santosha.no`
- proof tier: `orgnr_on_page`
- identity level: `VERIFIED`
- automated verdict: **correct**

Source: https://www.santosha.no/

Retrieved: 2026-11-16T17:04:06.445866Z; SHA-256 `e2759a348859a9e370e18d69671a3608c208b3648ef56ed018b17e814eda6227`; locator `identity-proof:917571163`; method `signalpost.website.v1`.

<pre>ext__text"&gt;Copyright 2026 &amp;copy; Santosha AS 917 571 163&lt;/span&gt;&lt;/p&gt;&lt;/div&gt;&lt;/div&gt;&lt;/div&gt;&lt;/div&gt;&lt;div id="comp-mnz8ohrh5" class="comp-mnz8ohrh5 FDI5TK wixui</pre>

### 919293748 - YES SEAFISHING NORWAY SA - website

- url: `https://www.yesseafishing.no`
- proof tier: `orgnr_on_page`
- identity level: `VERIFIED`
- automated verdict: **correct**

Source: https://www.yesseafishing.no/

Retrieved: 2026-11-16T17:06:42.493911Z; SHA-256 `d4f16e1bd57d8fe3ddb03575c5f78a40c634e50cb5f00e07f32b588d1e6a8316`; locator `identity-proof:919293748`; method `signalpost.website.v1`.

<pre>e-local-99-text" style="color:"&gt;Org.nr. 919 293 748&lt;/span&gt;&lt;/div&gt;&lt;div class="last-el-spacer position-relative wp-block-kubio-iconlistitem__divider-wrap</pre>

Source: https://www.yesseafishing.no/

Retrieved: 2026-11-16T17:06:42.493911Z; SHA-256 `d4f16e1bd57d8fe3ddb03575c5f78a40c634e50cb5f00e07f32b588d1e6a8316`; locator `registry-contact:email_domain`; method `signalpost.registry_contact.v1`.

<pre>&lt;a href="mailto:post@yesseafishing.no" class="position-relative wp-block-kubio-iconlistitem__ style-OICeXxyOCi- style-local-95-"&gt;</pre>

### 926816179 - LUDVIG KAMPERHAUG AS - website

- url: `https://ludvigkamperhaug.no`
- proof tier: `orgnr_on_page`
- identity level: `VERIFIED`
- automated verdict: **correct**

Source: https://ludvigkamperhaug.no/kontakt-oss/

Retrieved: 2026-11-16T17:03:37.989515Z; SHA-256 `314fc0e0fcd09175b7cfbd6fcf71ea1a8fcba7308a797a8b523cea82ad73fd4b`; locator `identity-proof:926816179`; method `signalpost.website.v1`.

<pre>s="elementor-icon-list-text"&gt;Org.nr. NO 926 816 179 MVA&lt;/span&gt;
									&lt;/li&gt;
						&lt;/ul&gt;
						&lt;/div&gt;
				&lt;/div&gt;
				&lt;div class="elementor-element el</pre>

Source: https://ludvigkamperhaug.no/kontakt-oss/

Retrieved: 2026-11-16T17:03:37.989515Z; SHA-256 `314fc0e0fcd09175b7cfbd6fcf71ea1a8fcba7308a797a8b523cea82ad73fd4b`; locator `registry-contact:phone`; method `signalpost.registry_contact.v1`.

<pre>&lt;a href="tel:+4769144377"&gt;</pre>

Source: https://ludvigkamperhaug.no/kontakt-oss/

Retrieved: 2026-11-16T17:03:37.989515Z; SHA-256 `314fc0e0fcd09175b7cfbd6fcf71ea1a8fcba7308a797a8b523cea82ad73fd4b`; locator `registry-contact:email_domain`; method `signalpost.registry_contact.v1`.

<pre>&lt;a href="mailto:post@ludvigkamperhaug.no"&gt;</pre>

### 927612372 - CONTUR AS - website

- url: `https://contur.no`
- proof tier: `orgnr_on_page`
- identity level: `VERIFIED`
- automated verdict: **correct**

Source: https://contur.no/kontakt/

Retrieved: 2026-11-16T17:07:03.487240Z; SHA-256 `18828a0f965f29c11e98bfe2794ffd30fb030df2e090df869301e88a4fd70d1a`; locator `identity-proof:927612372`; method `signalpost.website.v1`.

<pre>ich-text"&gt;&lt;h3&gt;Contur AS&lt;/h3&gt;
&lt;p&gt;Org.nr. 927 612 372&lt;/p&gt;
&lt;p&gt;&lt;strong&gt;Adresse:&lt;/strong&gt;&lt;br /&gt;
Vige Havnevei 4, 4. etg.&lt;br /&gt;
4633 Kristiansand&lt;/p&gt;
&lt;p&gt;Tel</pre>

### 928003027 - LUNE BYGG AS - website

- url: `https://lunebygg.no`
- proof tier: `orgnr_on_page`
- identity level: `VERIFIED`
- automated verdict: **correct**

Source: https://lunebygg.no/

Retrieved: 2026-11-16T17:04:01.032882Z; SHA-256 `e0e070826f5e0e6763c5a1cb213d88c192b6f1c1e328df74c22d08d98aea3be2`; locator `identity-proof:928003027`; method `signalpost.website.v1`.

<pre>-2xl"&gt;Bedrift&lt;/h1&gt;&lt;p&gt;Foretaksnummer: NO 928 003 027 MVA&lt;/p&gt;&lt;p&gt;Adresse: Bjørkedalvegen 700, 3948 Porsgrunn&lt;/p&gt;&lt;/div&gt;&lt;/div&gt;&lt;div class="         row-star</pre>

### 934369165 - BRETUN TAK AS - website

- url: `https://bretuntak.no`
- proof tier: `orgnr_on_page`
- identity level: `VERIFIED`
- automated verdict: **correct**

Source: https://bretuntak.no/

Retrieved: 2026-11-16T17:05:38.117464Z; SHA-256 `6ffb5df212c4b1795a1ad34b764f6e55784812c45cf289f7089bc95c1a2fc70e`; locator `identity-proof:934369165`; method `signalpost.website.v1`.

<pre> data-interaction-id="48d2d366"&gt;Org.nr. 934 369 165&lt;/span&gt;
					&lt;span class="btn-tekst-lys-d6509 e-paragraph-base e-default-span" data-interaction-id=</pre>

### 935254302 - LJOMAHUD AS - website

- url: `https://ljomahud.no`
- proof tier: `orgnr_on_page`
- identity level: `VERIFIED`
- automated verdict: **correct**

Source: https://ljomahud.no/

Retrieved: 2026-11-16T17:07:20.487794Z; SHA-256 `ec3f9884c259572d3698f90fb94d20ebcfc8ce308b7e4573d5e7ed940a01a385`; locator `identity-proof:935254302`; method `signalpost.website.v1`.

<pre>Karl Johans gate 23-LJOMAHUD AS ORG NR: 935254302
                              &lt;/span&gt;
                            &lt;/p&gt;

                      &lt;/div&gt;</pre>

### 935834872 - AML AUTO AS - website

- url: `https://amlauto.no`
- proof tier: `orgnr_on_page`
- identity level: `VERIFIED`
- automated verdict: **correct**

Source: https://amlauto.no/

Retrieved: 2026-11-16T17:06:54.092194Z; SHA-256 `1a43eaee5be266da73936887228e11d985b5dbe708321ff4980d982911c24243`; locator `identity-proof:935834872`; method `signalpost.website.v1`.

<pre> id="year"&gt;&lt;/span&gt;AML Auto AS | Org.nr: 935 834 872&lt;/span&gt;
&lt;/div&gt;
&lt;/footer&gt;
&lt;script&gt;
  const el = document.getElementById('inventory');
  const q = do</pre>

### 936235891 - GULLBEKK VISUALS AS - website

- url: `https://www.gullbekkvisuals.no`
- proof tier: `orgnr_on_page`
- identity level: `VERIFIED`
- automated verdict: **correct**

Source: https://www.gullbekkvisuals.no/

Retrieved: 2026-11-16T17:06:40.106336Z; SHA-256 `778586954a221e9a0ce5c7ad2eadff52ce2201acb742d0e39e296df091178067`; locator `identity-proof:936235891`; method `signalpost.website.v1`.

<pre>6&lt;!-- --&gt; Gullbekk Visuals AS · Org.nr: 936 235 891 MVA&lt;/p&gt;&lt;div class="flex flex-wrap gap-4 md:gap-6"&gt;&lt;a class="text-[10px] uppercase tracking-widest </pre>

### 975977161 - GUNILLAS HELSEKOST AS - website

- url: `https://gunillas.no`
- proof tier: `orgnr_on_page`
- identity level: `VERIFIED`
- automated verdict: **correct**

Source: https://gunillas.no/vilkar-og-retningslinjer/

Retrieved: 2026-11-16T17:03:58.558271Z; SHA-256 `b30654504629f98b0fbf826c779e9bf0a9cfb4d82f3f5965512d1941d2107b3d`; locator `identity-proof:975977161`; method `signalpost.website.v1`.

<pre>rgba(0, 0, 0, 0);"&gt;Organisasjonsnummer: 975 977 161&lt;br /&gt;&lt;/span&gt;&lt;span style="letter-spacing: 0.7px; background-color: rgba(0, 0, 0, 0);"&gt;Adresse: Kong</pre>

### 980387364 - BEST MILJØ AS - website

- url: `https://www.bestmiljo.no`
- proof tier: `orgnr_on_page`
- identity level: `VERIFIED`
- automated verdict: **correct**

Source: https://www.bestmiljo.no/

Retrieved: 2026-11-16T17:04:21.314663Z; SHA-256 `96d5b988545f783aded04415e8c54b265a3b5598c1c182a5f607bd7341d38b23`; locator `identity-proof:980387364`; method `signalpost.website.v1`.

<pre>ke-linejoin="round"&gt;&lt;/path&gt;&lt;/svg&gt;Org.nr 980 387 364&lt;/li&gt;&lt;/ul&gt;&lt;/div&gt;&lt;/div&gt;&lt;section class="bg-[#3a3d36] px-4 py-12 md:px-6 md:py-14"&gt;&lt;div class="mx-auto</pre>

### 985644446 - STIFTELSESFORENINGEN - website

- url: `https://stiftelsesforeningen.no`
- proof tier: `orgnr_on_page`
- identity level: `VERIFIED`
- automated verdict: **correct**

Source: https://stiftelsesforeningen.no/

Retrieved: 2026-11-16T17:06:00.776756Z; SHA-256 `d592ab3b68080ee3ba6e4b9df8b0eaed00568ecedb9952f4e2569827819cf4b7`; locator `identity-proof:985644446`; method `signalpost.website.v1`.

<pre>foreningen&lt;/h2&gt;&lt;ul&gt;&lt;li&gt;Org. nr. &lt;!-- --&gt;985 644 446&lt;/li&gt;&lt;/ul&gt;&lt;/div&gt;&lt;div&gt;&lt;h3&gt;Kontakt oss&lt;/h3&gt;&lt;div class="body-module-scss-module__fMrSDG__body" data-wi</pre>

Source: https://stiftelsesforeningen.no/

Retrieved: 2026-11-16T17:06:00.776756Z; SHA-256 `d592ab3b68080ee3ba6e4b9df8b0eaed00568ecedb9952f4e2569827819cf4b7`; locator `registry-contact:email_domain`; method `signalpost.registry_contact.v1`.

<pre>&lt;a href="mailto:post@stiftelsesforeningen.no" target="_blank" rel="noopener noreferrer"&gt;</pre>

### 992595485 - KROG BOLIG AS - website

- url: `https://www.krogbolig.no`
- proof tier: `orgnr_on_page`
- identity level: `VERIFIED`
- automated verdict: **correct**

Source: https://www.krogbolig.no/

Retrieved: 2026-11-16T17:06:25.436051Z; SHA-256 `54255ca3f5ffd3e289280cd2ce3ee8fa690af554e269e61d76e9ffa5e9069ecc`; locator `identity-proof:992595485`; method `signalpost.website.v1`.

<pre>&lt;span class="C9DxTc " style=""&gt;Org. nr. 992595485&lt;/span&gt;&lt;/small&gt;&lt;small id="h.r5ym7z4vmrfv" dir="ltr" class="zfr3Q TMjjoe CDt4Ke " style="display: bloc</pre>

### 993093335 - BLOMSTER I BYHAVEN AS - website

- url: `https://www.byblomst.no`
- proof tier: `orgnr_on_page`
- identity level: `VERIFIED`
- automated verdict: **correct**

Source: https://www.byblomst.no/

Retrieved: 2026-11-16T17:03:53.099861Z; SHA-256 `8f3b2fafd8b6a27aa476d4533cc7544671fbf206403ac8dcd4c3415596407a41`; locator `identity-proof:993093335`; method `signalpost.website.v1`.

<pre>                            &lt;p&gt;Org.nr.: 993093335&lt;/p&gt;
            &lt;p&gt;&lt;/p&gt;
        &lt;/span&gt;
            &lt;/div&gt;
      
            &lt;ul class="footer__lin</pre>

Source: https://www.byblomst.no/

Retrieved: 2026-11-16T17:03:53.099861Z; SHA-256 `8f3b2fafd8b6a27aa476d4533cc7544671fbf206403ac8dcd4c3415596407a41`; locator `registry-contact:email_domain`; method `signalpost.registry_contact.v1`.

<pre>&lt;a  href="mailto:butikk@byblomst.no" class="footer__link"&gt;</pre>

### 998530709 - PRIMATOSCANA AS - website

- url: `https://primatoscana.no`
- proof tier: `orgnr_on_page`
- identity level: `VERIFIED`
- automated verdict: **correct**

Source: https://primatoscana.no/om-oss/

Retrieved: 2026-11-16T17:04:20.649875Z; SHA-256 `9238e281e1a0029801d1bee4fdde173cf7f39f80aaae0a945db92069c9faf8a6`; locator `identity-proof:998530709`; method `signalpost.website.v1`.

<pre>
&lt;p class="wp-block-paragraph"&gt;org. nr: 998 530 709&lt;/p&gt;



&lt;h2 class="wp-block-heading"&gt;&lt;/h2&gt;
&lt;/div&gt;



&lt;div class="wp-block-column is-layout-flow wp-</pre>

### 999654495 - PRODECO AS - website

- url: `https://prodeco.no`
- proof tier: `orgnr_on_page`
- identity level: `VERIFIED`
- automated verdict: **correct**

Source: https://prodeco.no/kontakt/

Retrieved: 2026-11-16T17:03:51.818957Z; SHA-256 `531b3a4c563291a291d60b291de40ab2c6ff002127359fbae7c7f69ed3ee699a`; locator `identity-proof:999654495`; method `signalpost.website.v1`.

<pre>lass="button"&gt;
        &lt;span&gt;Org.nr: NO 999 654 495&lt;/span&gt;
      &lt;/a&gt;
                  &lt;/div&gt;
                  &lt;/div&gt;
      &lt;/div&gt;
    &lt;/section&gt;
  </pre>

## Social — automated correct (14)

### 813587912 - FUSA LYD & LYS AS - social

- url: `https://www.facebook.com/fusalydlys`
- proof tier: `own_header_footer_exact_name_v1`
- automated verdict: **correct**

Source: https://www.fusalydlys.no/

Retrieved: 2026-11-16T17:41:27.422493Z; SHA-256 `69dd14e12b094efac98eedc487a69c88043099c639d376f99763038be2fffc04`; locator `company-link:https://www.facebook.com/fusalydlys`; method `signalpost.website.v1`.

<pre>&lt;a href="https://www.facebook.com/fusalydlys" target="_blank" rel="noreferrer" title="Facebook"&gt;</pre>

Source: https://www.fusalydlys.no/

Retrieved: 2026-11-16T17:41:27.422493Z; SHA-256 `69dd14e12b094efac98eedc487a69c88043099c639d376f99763038be2fffc04`; locator `identity-proof:813587912`; method `signalpost.website.v1`.

<pre> 97 71 16 87 / 92 67 05 48&lt;/p&gt;&lt;p&gt;Org.nr 813 587 912&lt;/p&gt;
&lt;/div&gt;
&lt;/div&gt;&lt;/div&gt;
&lt;/div&gt;&lt;div class="c cf" style="width:19.139%;"&gt;
	&lt;div class="c-c cf"&gt;&lt;d</pre>

### 897198452 - VERDIHUSET AS - social

- url: `https://www.facebook.com/verdihuset`
- proof tier: `own_header_footer_exact_name_v1`
- automated verdict: **correct**

Source: https://www.verdihuset.no/

Retrieved: 2026-11-16T17:04:47.356120Z; SHA-256 `24215c66b315bfab23146ee68ce450c7212071dafc3af243b13c3647c461d6a9`; locator `company-link:https://www.facebook.com/verdihuset`; method `signalpost.website.v1`.

<pre>&lt;a href="https://www.facebook.com/verdihuset/" target="_blank"&gt;</pre>

Source: https://www.verdihuset.no/

Retrieved: 2026-11-16T17:04:47.356120Z; SHA-256 `24215c66b315bfab23146ee68ce450c7212071dafc3af243b13c3647c461d6a9`; locator `identity-proof:897198452`; method `signalpost.website.v1`.

<pre>ey="paragraph"&gt;
            &lt;p&gt;Org. nr: 897198452&lt;/p&gt;&lt;p&gt;Adresse:&lt;br&gt;Ski: Bråtenveien 3, 1423 Ski&lt;br&gt;Bergen: Storetveitvegen 22, 5067 Bergen&lt;/p&gt;&lt;p&gt;E-po</pre>

Source: https://www.verdihuset.no/

Retrieved: 2026-11-16T17:04:47.356120Z; SHA-256 `24215c66b315bfab23146ee68ce450c7212071dafc3af243b13c3647c461d6a9`; locator `registry-contact:phone`; method `signalpost.registry_contact.v1`.

<pre>er06.01.265.jpg",
        "telephone": "410 88 888",
        "contactPoint": {
            "@type": "ContactPoint",
            "telephone": "410 88 888",
            "contactType": "NO",
            "areaServed": "NO",
            "availableLanguage": "no",
            "url": "https://www.verdihuse</pre>

### 897198452 - VERDIHUSET AS - social

- url: `https://www.instagram.com/verdihuset`
- proof tier: `own_header_footer_exact_name_v1`
- automated verdict: **correct**

Source: https://www.verdihuset.no/

Retrieved: 2026-11-16T17:04:47.356120Z; SHA-256 `24215c66b315bfab23146ee68ce450c7212071dafc3af243b13c3647c461d6a9`; locator `company-link:https://www.instagram.com/verdihuset`; method `signalpost.website.v1`.

<pre>&lt;a href="https://www.instagram.com/verdihuset/"&gt;</pre>

Source: https://www.verdihuset.no/

Retrieved: 2026-11-16T17:04:47.356120Z; SHA-256 `24215c66b315bfab23146ee68ce450c7212071dafc3af243b13c3647c461d6a9`; locator `identity-proof:897198452`; method `signalpost.website.v1`.

<pre>ey="paragraph"&gt;
            &lt;p&gt;Org. nr: 897198452&lt;/p&gt;&lt;p&gt;Adresse:&lt;br&gt;Ski: Bråtenveien 3, 1423 Ski&lt;br&gt;Bergen: Storetveitvegen 22, 5067 Bergen&lt;/p&gt;&lt;p&gt;E-po</pre>

Source: https://www.verdihuset.no/

Retrieved: 2026-11-16T17:04:47.356120Z; SHA-256 `24215c66b315bfab23146ee68ce450c7212071dafc3af243b13c3647c461d6a9`; locator `registry-contact:phone`; method `signalpost.registry_contact.v1`.

<pre>er06.01.265.jpg",
        "telephone": "410 88 888",
        "contactPoint": {
            "@type": "ContactPoint",
            "telephone": "410 88 888",
            "contactType": "NO",
            "areaServed": "NO",
            "availableLanguage": "no",
            "url": "https://www.verdihuse</pre>

### 926816179 - LUDVIG KAMPERHAUG AS - social

- url: `https://www.facebook.com/ludvigkamperhaug`
- proof tier: `own_header_footer_exact_name_v1`
- automated verdict: **correct**

Source: https://ludvigkamperhaug.no/

Retrieved: 2026-11-16T17:03:35.014187Z; SHA-256 `22ae7112455453e5c69f358c4286e3b16694fc80600ef3dc26d5f29c7de702a3`; locator `company-link:https://www.facebook.com/ludvigkamperhaug`; method `signalpost.website.v1`.

<pre>&lt;a class="elementor-icon elementor-social-icon elementor-social-icon-facebook-f elementor-repeater-item-320e991" href="https://www.facebook.com/ludvigkamperhaug/" target="_blank" rel="nofollow"&gt;</pre>

Source: https://ludvigkamperhaug.no/kontakt-oss/

Retrieved: 2026-11-16T17:03:37.989515Z; SHA-256 `314fc0e0fcd09175b7cfbd6fcf71ea1a8fcba7308a797a8b523cea82ad73fd4b`; locator `identity-proof:926816179`; method `signalpost.website.v1`.

<pre>s="elementor-icon-list-text"&gt;Org.nr. NO 926 816 179 MVA&lt;/span&gt;
									&lt;/li&gt;
						&lt;/ul&gt;
						&lt;/div&gt;
				&lt;/div&gt;
				&lt;div class="elementor-element el</pre>

Source: https://ludvigkamperhaug.no/kontakt-oss/

Retrieved: 2026-11-16T17:03:37.989515Z; SHA-256 `314fc0e0fcd09175b7cfbd6fcf71ea1a8fcba7308a797a8b523cea82ad73fd4b`; locator `registry-contact:phone`; method `signalpost.registry_contact.v1`.

<pre>&lt;a href="tel:+4769144377"&gt;</pre>

Source: https://ludvigkamperhaug.no/kontakt-oss/

Retrieved: 2026-11-16T17:03:37.989515Z; SHA-256 `314fc0e0fcd09175b7cfbd6fcf71ea1a8fcba7308a797a8b523cea82ad73fd4b`; locator `registry-contact:email_domain`; method `signalpost.registry_contact.v1`.

<pre>&lt;a href="mailto:post@ludvigkamperhaug.no"&gt;</pre>

### 927612372 - CONTUR AS - social

- url: `https://www.instagram.com/contur_as`
- proof tier: `own_header_footer_exact_name_v1`
- automated verdict: **correct**

Source: https://contur.no/

Retrieved: 2026-11-16T17:07:02.234350Z; SHA-256 `6f7ad07a4f9eee9fc0d9f96ab1d2b9ffdb7cfc4093f5521d76a25dadf6ceada4`; locator `company-link:https://www.instagram.com/contur_as`; method `signalpost.website.v1`.

<pre>&lt;a href="https://www.instagram.com/contur_as/" class="group"&gt;</pre>

Source: https://contur.no/kontakt/

Retrieved: 2026-11-16T17:07:03.487240Z; SHA-256 `18828a0f965f29c11e98bfe2794ffd30fb030df2e090df869301e88a4fd70d1a`; locator `identity-proof:927612372`; method `signalpost.website.v1`.

<pre>ich-text"&gt;&lt;h3&gt;Contur AS&lt;/h3&gt;
&lt;p&gt;Org.nr. 927 612 372&lt;/p&gt;
&lt;p&gt;&lt;strong&gt;Adresse:&lt;/strong&gt;&lt;br /&gt;
Vige Havnevei 4, 4. etg.&lt;br /&gt;
4633 Kristiansand&lt;/p&gt;
&lt;p&gt;Tel</pre>

### 935254302 - LJOMAHUD AS - social

- url: `https://www.facebook.com/Ljomahud`
- proof tier: `own_header_footer_exact_name_v1`
- automated verdict: **correct**

Source: https://ljomahud.no/

Retrieved: 2026-11-16T17:07:20.487794Z; SHA-256 `ec3f9884c259572d3698f90fb94d20ebcfc8ce308b7e4573d5e7ed940a01a385`; locator `company-link:https://www.facebook.com/Ljomahud`; method `signalpost.website.v1`.

<pre>&lt;a
            href="https://www.facebook.com/Ljomahud"
            title="Ljoma Hud på Facebook"
            target="_blank"
            rel="noopener"
          &gt;</pre>

Source: https://ljomahud.no/

Retrieved: 2026-11-16T17:07:20.487794Z; SHA-256 `ec3f9884c259572d3698f90fb94d20ebcfc8ce308b7e4573d5e7ed940a01a385`; locator `identity-proof:935254302`; method `signalpost.website.v1`.

<pre>Karl Johans gate 23-LJOMAHUD AS ORG NR: 935254302
                              &lt;/span&gt;
                            &lt;/p&gt;

                      &lt;/div&gt;</pre>

### 935254302 - LJOMAHUD AS - social

- url: `https://www.instagram.com/ljomahud`
- proof tier: `own_header_footer_exact_name_v1`
- automated verdict: **correct**

Source: https://ljomahud.no/

Retrieved: 2026-11-16T17:07:20.487794Z; SHA-256 `ec3f9884c259572d3698f90fb94d20ebcfc8ce308b7e4573d5e7ed940a01a385`; locator `company-link:https://www.instagram.com/ljomahud`; method `signalpost.website.v1`.

<pre>&lt;a
            href="https://www.instagram.com/ljomahud/"
            title="Ljoma Hud på Instagram"
            target="_blank"
            rel="noopener"
          &gt;</pre>

Source: https://ljomahud.no/

Retrieved: 2026-11-16T17:07:20.487794Z; SHA-256 `ec3f9884c259572d3698f90fb94d20ebcfc8ce308b7e4573d5e7ed940a01a385`; locator `identity-proof:935254302`; method `signalpost.website.v1`.

<pre>Karl Johans gate 23-LJOMAHUD AS ORG NR: 935254302
                              &lt;/span&gt;
                            &lt;/p&gt;

                      &lt;/div&gt;</pre>

### 936235891 - GULLBEKK VISUALS AS - social

- url: `https://instagram.com/gullbekkvisuals`
- proof tier: `own_header_footer_exact_name_v1`
- automated verdict: **correct**

Source: https://www.gullbekkvisuals.no/

Retrieved: 2026-11-16T17:06:40.106336Z; SHA-256 `778586954a221e9a0ce5c7ad2eadff52ce2201acb742d0e39e296df091178067`; locator `company-link:https://instagram.com/gullbekkvisuals`; method `signalpost.website.v1`.

<pre>&lt;a href="https://instagram.com/gullbekkvisuals" target="_blank" rel="noopener noreferrer" aria-label="Follow us on Instagram" class="text-[#F6F4F0]/70 hover:text-[#420604] transition-colors"&gt;</pre>

Source: https://www.gullbekkvisuals.no/

Retrieved: 2026-11-16T17:06:40.106336Z; SHA-256 `778586954a221e9a0ce5c7ad2eadff52ce2201acb742d0e39e296df091178067`; locator `identity-proof:936235891`; method `signalpost.website.v1`.

<pre>6&lt;!-- --&gt; Gullbekk Visuals AS · Org.nr: 936 235 891 MVA&lt;/p&gt;&lt;div class="flex flex-wrap gap-4 md:gap-6"&gt;&lt;a class="text-[10px] uppercase tracking-widest </pre>

### 985644446 - STIFTELSESFORENINGEN - social

- url: `https://www.facebook.com/stiftelsesforeningen`
- proof tier: `own_header_footer_exact_name_v1`
- automated verdict: **correct**

Source: https://stiftelsesforeningen.no/

Retrieved: 2026-11-16T17:06:00.776756Z; SHA-256 `d592ab3b68080ee3ba6e4b9df8b0eaed00568ecedb9952f4e2569827819cf4b7`; locator `company-link:https://www.facebook.com/stiftelsesforeningen`; method `signalpost.website.v1`.

<pre>&lt;a href="https://www.facebook.com/stiftelsesforeningen/" target="_blank"&gt;</pre>

Source: https://stiftelsesforeningen.no/

Retrieved: 2026-11-16T17:06:00.776756Z; SHA-256 `d592ab3b68080ee3ba6e4b9df8b0eaed00568ecedb9952f4e2569827819cf4b7`; locator `identity-proof:985644446`; method `signalpost.website.v1`.

<pre>foreningen&lt;/h2&gt;&lt;ul&gt;&lt;li&gt;Org. nr. &lt;!-- --&gt;985 644 446&lt;/li&gt;&lt;/ul&gt;&lt;/div&gt;&lt;div&gt;&lt;h3&gt;Kontakt oss&lt;/h3&gt;&lt;div class="body-module-scss-module__fMrSDG__body" data-wi</pre>

Source: https://stiftelsesforeningen.no/

Retrieved: 2026-11-16T17:06:00.776756Z; SHA-256 `d592ab3b68080ee3ba6e4b9df8b0eaed00568ecedb9952f4e2569827819cf4b7`; locator `registry-contact:email_domain`; method `signalpost.registry_contact.v1`.

<pre>&lt;a href="mailto:post@stiftelsesforeningen.no" target="_blank" rel="noopener noreferrer"&gt;</pre>

### 985644446 - STIFTELSESFORENINGEN - social

- url: `https://www.instagram.com/stiftelsesforeningen`
- proof tier: `own_header_footer_exact_name_v1`
- automated verdict: **correct**

Source: https://stiftelsesforeningen.no/

Retrieved: 2026-11-16T17:06:00.776756Z; SHA-256 `d592ab3b68080ee3ba6e4b9df8b0eaed00568ecedb9952f4e2569827819cf4b7`; locator `company-link:https://www.instagram.com/stiftelsesforeningen`; method `signalpost.website.v1`.

<pre>&lt;a href="https://www.instagram.com/stiftelsesforeningen/" target="_blank"&gt;</pre>

Source: https://stiftelsesforeningen.no/

Retrieved: 2026-11-16T17:06:00.776756Z; SHA-256 `d592ab3b68080ee3ba6e4b9df8b0eaed00568ecedb9952f4e2569827819cf4b7`; locator `identity-proof:985644446`; method `signalpost.website.v1`.

<pre>foreningen&lt;/h2&gt;&lt;ul&gt;&lt;li&gt;Org. nr. &lt;!-- --&gt;985 644 446&lt;/li&gt;&lt;/ul&gt;&lt;/div&gt;&lt;div&gt;&lt;h3&gt;Kontakt oss&lt;/h3&gt;&lt;div class="body-module-scss-module__fMrSDG__body" data-wi</pre>

Source: https://stiftelsesforeningen.no/

Retrieved: 2026-11-16T17:06:00.776756Z; SHA-256 `d592ab3b68080ee3ba6e4b9df8b0eaed00568ecedb9952f4e2569827819cf4b7`; locator `registry-contact:email_domain`; method `signalpost.registry_contact.v1`.

<pre>&lt;a href="mailto:post@stiftelsesforeningen.no" target="_blank" rel="noopener noreferrer"&gt;</pre>

### 985644446 - STIFTELSESFORENINGEN - social

- url: `https://www.linkedin.com/company/stiftelsesforeningen`
- proof tier: `own_header_footer_exact_name_v1`
- automated verdict: **correct**

Source: https://stiftelsesforeningen.no/

Retrieved: 2026-11-16T17:06:00.776756Z; SHA-256 `d592ab3b68080ee3ba6e4b9df8b0eaed00568ecedb9952f4e2569827819cf4b7`; locator `company-link:https://www.linkedin.com/company/stiftelsesforeningen`; method `signalpost.website.v1`.

<pre>&lt;a href="https://www.linkedin.com/company/stiftelsesforeningen" target="_blank"&gt;</pre>

Source: https://stiftelsesforeningen.no/

Retrieved: 2026-11-16T17:06:00.776756Z; SHA-256 `d592ab3b68080ee3ba6e4b9df8b0eaed00568ecedb9952f4e2569827819cf4b7`; locator `identity-proof:985644446`; method `signalpost.website.v1`.

<pre>foreningen&lt;/h2&gt;&lt;ul&gt;&lt;li&gt;Org. nr. &lt;!-- --&gt;985 644 446&lt;/li&gt;&lt;/ul&gt;&lt;/div&gt;&lt;div&gt;&lt;h3&gt;Kontakt oss&lt;/h3&gt;&lt;div class="body-module-scss-module__fMrSDG__body" data-wi</pre>

Source: https://stiftelsesforeningen.no/

Retrieved: 2026-11-16T17:06:00.776756Z; SHA-256 `d592ab3b68080ee3ba6e4b9df8b0eaed00568ecedb9952f4e2569827819cf4b7`; locator `registry-contact:email_domain`; method `signalpost.registry_contact.v1`.

<pre>&lt;a href="mailto:post@stiftelsesforeningen.no" target="_blank" rel="noopener noreferrer"&gt;</pre>

### 998530709 - PRIMATOSCANA AS - social

- url: `https://www.facebook.com/Primatoscana`
- proof tier: `own_header_footer_exact_name_v1`
- automated verdict: **correct**

Source: https://primatoscana.no/

Retrieved: 2026-11-16T17:04:15.236671Z; SHA-256 `385b3b977c1dd9d49f77160f6fab7127bf012cee2f1017790d50cbcf2bc86891`; locator `company-link:https://www.facebook.com/Primatoscana`; method `signalpost.website.v1`.

<pre>&lt;a href="https://www.facebook.com/Primatoscana" class="facebook-link" target="_blank"&gt;</pre>

Source: https://primatoscana.no/om-oss/

Retrieved: 2026-11-16T17:04:20.649875Z; SHA-256 `9238e281e1a0029801d1bee4fdde173cf7f39f80aaae0a945db92069c9faf8a6`; locator `identity-proof:998530709`; method `signalpost.website.v1`.

<pre>
&lt;p class="wp-block-paragraph"&gt;org. nr: 998 530 709&lt;/p&gt;



&lt;h2 class="wp-block-heading"&gt;&lt;/h2&gt;
&lt;/div&gt;



&lt;div class="wp-block-column is-layout-flow wp-</pre>

### 999654495 - PRODECO AS - social

- url: `https://www.instagram.com/prodecoas`
- proof tier: `own_header_footer_exact_name_v1`
- automated verdict: **correct**

Source: https://prodeco.no/

Retrieved: 2026-11-16T17:03:49.271707Z; SHA-256 `1beb08bf1e51f74252494ee8f3875f4bc7ed87450c16ec0b6c717034af872f24`; locator `company-link:https://www.instagram.com/prodecoas`; method `signalpost.website.v1`.

<pre>&lt;a href="https://www.instagram.com/prodecoas/" rel="noopener" target="_blank"&gt;</pre>

Source: https://prodeco.no/kontakt/

Retrieved: 2026-11-16T17:03:51.818957Z; SHA-256 `531b3a4c563291a291d60b291de40ab2c6ff002127359fbae7c7f69ed3ee699a`; locator `identity-proof:999654495`; method `signalpost.website.v1`.

<pre>lass="button"&gt;
        &lt;span&gt;Org.nr: NO 999 654 495&lt;/span&gt;
      &lt;/a&gt;
                  &lt;/div&gt;
                  &lt;/div&gt;
      &lt;/div&gt;
    &lt;/section&gt;
  </pre>

### 999654495 - PRODECO AS - social

- url: `https://www.linkedin.com/company/prodeco-as`
- proof tier: `own_header_footer_exact_name_v1`
- automated verdict: **correct**

Source: https://prodeco.no/

Retrieved: 2026-11-16T17:03:49.271707Z; SHA-256 `1beb08bf1e51f74252494ee8f3875f4bc7ed87450c16ec0b6c717034af872f24`; locator `company-link:https://www.linkedin.com/company/prodeco-as`; method `signalpost.website.v1`.

<pre>&lt;a href="https://www.linkedin.com/company/prodeco-as/" rel="noopener" target="_blank"&gt;</pre>

Source: https://prodeco.no/kontakt/

Retrieved: 2026-11-16T17:03:51.818957Z; SHA-256 `531b3a4c563291a291d60b291de40ab2c6ff002127359fbae7c7f69ed3ee699a`; locator `identity-proof:999654495`; method `signalpost.website.v1`.

<pre>lass="button"&gt;
        &lt;span&gt;Org.nr: NO 999 654 495&lt;/span&gt;
      &lt;/a&gt;
                  &lt;/div&gt;
                  &lt;/div&gt;
      &lt;/div&gt;
    &lt;/section&gt;
  </pre>
