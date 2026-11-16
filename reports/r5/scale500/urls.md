# P2 scale-500 published website/social inventory

Seed 20261118, 500 companies disjoint from every committed sample, run `r5-scale500-seed20261118-final` from a clean clone. Every published website and social URL is listed with exact saved excerpts, proof tier, retrieval time and SHA-256; each receipt was re-hashed from the saved body and its excerpt found verbatim. Automated verdicts use the existing offline precision-ledger rules (scripts/precision_ledger.py `recheck`); they are rule checks, not human verdicts.

| Kind | Correct | Doubtful | Wrong |
|---|---:|---:|---:|
| website | 23 | 13 | 1 |
| social | 10 | 1 | 5 |

Automated labels are shown exactly as produced. 6 "wrong" label(s) are ledger-tool limitations, not identity findings: `StopIteration` means the legacy recheck found no HTML identity receipt because the site was proven from a linked legal PDF (Stage L2), and "no longer verifies" on `owner_jsonld_sameas_v1` / `own_contact_follow_us_v1` means the legacy social recheck predates the X2 owner-declaration tiers. The full independent verifier (`check_live_run.py`, including `verify_legal_pdf` and `verify_owner_social`) passed every one of them. They stay listed for hand-check below.

## Automated-doubtful or wrong — for hand-check (20)

### 918811370 - TOTEN FORSIKRING AS - social

- url: `https://www.facebook.com/totenforsikring`
- proof tier: `own_header_footer_exact_name_v1`
- automated verdict: **wrong** (StopIteration)

Source: https://totenforsikring.no/

Retrieved: 2026-11-16T08:27:39.033094Z; SHA-256 `6046fb1ff611f2f9555a0765a481f0d009bc337d8246c53c1eb8f7d94249baa5`; locator `company-link:https://www.facebook.com/totenforsikring`; method `signalpost.website.v1`.

<pre>&lt;a id="link-260-37" class="ct-link" href="https://www.facebook.com/totenforsikring" target="_blank"  &gt;</pre>

Source: https://totenforsikring.no/wp-content/uploads/2023/03/Angreskjema-Toten-2.pdf

Retrieved: 2026-11-16T08:27:52.570456Z; SHA-256 `5b3f3b24a0c229693c279133aad7fee2f165360228e082b3e79ddfe73ccf1133`; locator `pdf:page:1/identity-proof:918811370`; method `signalpost.website.v1`.

<pre>oten Forsikring AS
Organisasjonsnummer 
918811370  
Telefonnummer Adresse 
Jernbanesvingen 6, 2821 Gjøvik 990 13 282 
E-postadresse 
service@totenfors</pre>

Source: https://totenforsikring.no/wp-content/uploads/2023/03/Angreskjema-Toten-2.pdf

Retrieved: 2026-11-16T08:27:52.570456Z; SHA-256 `d0347d389a513abb5c91b1725f03df05e132d2db6638ebc6e8a486efc557bdd6`; locator `pdf:original`; method `signalpost.legal_pdf.v1`.

<pre>%PDF-</pre>

Source: https://totenforsikring.no/angrerett/

Retrieved: 2026-11-16T08:27:50.423327Z; SHA-256 `3eb9ede087a662a9022ff0eda91e219189b16fff277aac89518a1c2844c888ab`; locator `legal-pdf-link:https://totenforsikring.no/wp-content/uploads/2023/03/Angreskjema-Toten-2.pdf`; method `signalpost.legal_pdf.v1`.

<pre>&lt;a id="link_text-125-365" class="ct-link-text" href="https://totenforsikring.no/wp-content/uploads/2023/03/Angreskjema-Toten-2.pdf" target="_blank"  &gt;</pre>

### 922569738 - SNUOM PSYKISK HELSE AS - social

- url: `https://www.instagram.com/snuompsykiskhelse`
- proof tier: `own_header_footer_exact_name_v1`
- automated verdict: **doubtful** (No exact target orgnr in saved owner/proof context; published signal-only tier requires hand review; Published identity tier is below exact-number VERIFIED; Saved page proof needs review: corroboration)

Source: https://www.snuom.no/

Retrieved: 2026-11-16T08:33:46.896503Z; SHA-256 `48ffa66134daa87df8d84032e137f3daca0d8f1ba8e064fce523db912a54fd49`; locator `company-link:https://www.instagram.com/snuompsykiskhelse`; method `signalpost.website.v1`.

<pre>&lt;a data-testid="linkElement" href="https://www.instagram.com/snuompsykiskhelse/" target="_blank" rel="noreferrer noopener" class="FvIvPq" aria-label="Instagram     "&gt;</pre>

Source: https://www.snuom.no/

Retrieved: 2026-11-16T08:33:46.896503Z; SHA-256 `48ffa66134daa87df8d84032e137f3daca0d8f1ba8e064fce523db912a54fd49`; locator `identity-proof:922569738`; method `signalpost.website.v1`.

<pre>h2 class="font_2 wixui-rich-text__text"&gt;Snuom Psykisk Helse AS er en privat klinikk. Vi samarbeider tett med fastleger, forsikringsselskap og arbeidsgivere, og tilbyr rask oppstart uten henvisning eller ventetid i det offentlige systemet.&lt;/h2&gt;&lt;/div&gt;&lt;!--/$--&gt;&lt;/div&gt;&lt;!--/$--&gt;&lt;/div&gt;&lt;!--/$--&gt;&lt;/div&gt;&lt;/div&gt;</pre>

Source: https://www.snuom.no/

Retrieved: 2026-11-16T08:33:46.896503Z; SHA-256 `48ffa66134daa87df8d84032e137f3daca0d8f1ba8e064fce523db912a54fd49`; locator `registry-contact:phone`; method `signalpost.registry_contact.v1`.

<pre>&lt;a data-testid="linkElement" href="tel:+47 74 38 85 00" class="PoVCDy wixui-button ZhVEJq" aria-disabled="false" aria-label="Ring oss"&gt;</pre>

Source: https://www.snuom.no/

Retrieved: 2026-11-16T08:33:46.896503Z; SHA-256 `48ffa66134daa87df8d84032e137f3daca0d8f1ba8e064fce523db912a54fd49`; locator `registry-contact:email_domain`; method `signalpost.registry_contact.v1`.

<pre>&lt;a href="mailto:post@snuom.no?subject=Book time" target="_self" class="wixui-rich-text__text"&gt;</pre>

### 927361426 - L TERRASSE AS - social

- url: `https://www.facebook.com/Lterrasseno-101890795424991`
- proof tier: `owner_jsonld_sameas_v1`
- automated verdict: **wrong** (own header/footer/name/numeric-link policy no longer verifies)

Source: https://lterrasse.no/

Retrieved: 2026-11-16T08:36:57.115731Z; SHA-256 `fb2f834560b9477a2392e9e0232b3a884f6ab0c4c48309c5869b46881ccd60c1`; locator `company-link:https://www.facebook.com/Lterrasseno-101890795424991`; method `signalpost.website.v1`.

<pre>e":"L Terrasse AS","url":"https://lterrasse.no/","sameAs":["https://www.facebook.com/Lterrasseno-101890795424991/"],"logo":{"@type":"ImageObject","inLanguage":"nb-NO","@id":</pre>

Source: https://lterrasse.no/

Retrieved: 2026-11-16T08:36:57.115731Z; SHA-256 `fb2f834560b9477a2392e9e0232b3a884f6ab0c4c48309c5869b46881ccd60c1`; locator `identity-proof:927361426`; method `signalpost.website.v1`.

<pre>gen 10&lt;br /&gt;
7900 RØRVIK&lt;br /&gt;
Org. nr. 927 361 426&lt;/p&gt;
&lt;/div&gt;
		&lt;/div&gt;				&lt;/div&gt;
			
					&lt;/div&gt;
	&lt;/div&gt;
&lt;/footer&gt;
		
		
&lt;div id="bottom" clas</pre>

### 933831922 - SHIFT SECURITY AS - social

- url: `http://www.youtube.com/@ShiftSecurityAS`
- proof tier: `own_contact_follow_us_v1`
- automated verdict: **wrong** (own header/footer/name/numeric-link policy no longer verifies)

Source: https://shiftsecurity.no/kontakt

Retrieved: 2026-11-16T08:31:31.284021Z; SHA-256 `ee902aa3261d5dbe452217da135bda4e7777aa2ee36611fdea7e63745eb91709`; locator `company-link:http://www.youtube.com/@ShiftSecurityAS`; method `signalpost.website.v1`.

<pre>&lt;a href="http://www.youtube.com/@ShiftSecurityAS" rel="noopener"&gt;</pre>

Source: https://shiftsecurity.no/personvernerklaring

Retrieved: 2026-11-16T08:31:28.536856Z; SHA-256 `fe56c5e23d3778e10d3c0b193e242a2799f3a57b8262808e022be4fb2822ab72`; locator `identity-proof:933831922`; method `signalpost.website.v1`.

<pre>ift Security AS&lt;br&gt;Organisasjonsnummer: 933 831 922&lt;br&gt;E-post: &lt;a href="mailto:post@shiftsecurity.no" rel="noopener"&gt;post@shiftsecurity.no&lt;/a&gt;&lt;/span&gt;&lt;</pre>

### 933831922 - SHIFT SECURITY AS - social

- url: `https://www.youtube.com/@ShiftSecurityAS`
- proof tier: `own_contact_follow_us_v1`
- automated verdict: **wrong** (own header/footer/name/numeric-link policy no longer verifies)

Source: https://shiftsecurity.no/kontakt

Retrieved: 2026-11-16T08:31:31.284021Z; SHA-256 `ee902aa3261d5dbe452217da135bda4e7777aa2ee36611fdea7e63745eb91709`; locator `company-link:https://www.youtube.com/@ShiftSecurityAS`; method `signalpost.website.v1`.

<pre>&lt;a href="https://www.youtube.com/@ShiftSecurityAS" rel="noopener"&gt;</pre>

Source: https://shiftsecurity.no/personvernerklaring

Retrieved: 2026-11-16T08:31:28.536856Z; SHA-256 `fe56c5e23d3778e10d3c0b193e242a2799f3a57b8262808e022be4fb2822ab72`; locator `identity-proof:933831922`; method `signalpost.website.v1`.

<pre>ift Security AS&lt;br&gt;Organisasjonsnummer: 933 831 922&lt;br&gt;E-post: &lt;a href="mailto:post@shiftsecurity.no" rel="noopener"&gt;post@shiftsecurity.no&lt;/a&gt;&lt;/span&gt;&lt;</pre>

### 971050756 - ACCELLA SOLUTIONS AS - social

- url: `https://www.linkedin.com/company/petroonline-as`
- proof tier: `owner_jsonld_sameas_v1`
- automated verdict: **wrong** (own header/footer/name/numeric-link policy no longer verifies)

Source: https://accella.no/

Retrieved: 2026-11-16T08:35:41.607895Z; SHA-256 `29222d28f69806a90fffe46bb802ecb081987fe6a988e695aea32e2331449573`; locator `company-link:https://www.linkedin.com/company/petroonline-as`; method `signalpost.website.v1`.

<pre>https:\/\/accella.no\/#\/schema\/logo\/image\/"},"sameAs":["https:\/\/www.linkedin.com\/company\/petroonline-as\/"]}]}</pre>

Source: https://accella.no/

Retrieved: 2026-11-16T08:35:41.607895Z; SHA-256 `29222d28f69806a90fffe46bb802ecb081987fe6a988e695aea32e2331449573`; locator `identity-proof:971050756`; method `signalpost.website.v1`.

<pre>ass="elementor-icon-list-text"&gt;Org.nr.: 971.050.756&lt;/span&gt;
									&lt;/li&gt;
						&lt;/ul&gt;
						&lt;/div&gt;
				&lt;/div&gt;
					&lt;/div&gt;
		&lt;/div&gt;
				&lt;div class="ele</pre>

Source: https://accella.no/

Retrieved: 2026-11-16T08:35:41.607895Z; SHA-256 `29222d28f69806a90fffe46bb802ecb081987fe6a988e695aea32e2331449573`; locator `registry-contact:phone`; method `signalpost.registry_contact.v1`.

<pre>&lt;a href="tel:+4723060340"&gt;</pre>

### 816235502 - INDUSTRISTÅL AS - website

- url: `https://www.industristal.no`
- proof tier: `signals`
- identity level: `HIGH`
- automated verdict: **doubtful** (No exact target orgnr in saved owner/proof context; published signal-only tier requires hand review; Published identity tier is below exact-number VERIFIED; Saved page proof needs review: corroboration)

Source: https://www.industristal.no/

Retrieved: 2026-11-16T08:29:40.208885Z; SHA-256 `6f60f174ece30cf3f1e6f20fa1821ff88b516230da8ae9895cce60d05d8131ac`; locator `identity-proof:816235502`; method `signalpost.website.v1`.

<pre>sition:absolute;inset:0}&lt;/style&gt;
&lt;title&gt;Industristål AS - Stållageret Telemark alt innen stål&lt;/title&gt;
  &lt;meta name="description" content="Velkomen til oss. Alt innen for Stål. Vann, plasma, gass, laserskjæring, kantpresse, vals, Rør Bøying. Agentur Waltech og Buktens AB "/&gt;
  &lt;link rel="canonical" h</pre>

Source: https://www.industristal.no/

Retrieved: 2026-11-16T08:29:40.208885Z; SHA-256 `6f60f174ece30cf3f1e6f20fa1821ff88b516230da8ae9895cce60d05d8131ac`; locator `registry-contact:email_domain`; method `signalpost.registry_contact.v1`.

<pre>&lt;a data-auto-recognition="true" href="mailto:post@industristal.no" class="wixui-rich-text__text"&gt;</pre>

### 818003072 - INNOSAFE AS - website

- url: `https://www.molliesafe.no`
- proof tier: `registry_declared_live`
- identity level: `HIGH`
- automated verdict: **doubtful** (No exact target orgnr in saved owner/proof context; published signal-only tier requires hand review; Published identity tier is below exact-number VERIFIED; Saved page proof needs review: corroboration; Exact registry legal/brand spelling not located in saved page text)

Source: https://www.molliesafe.no/

Retrieved: 2026-11-16T08:29:59.510641Z; SHA-256 `6c84e23bb5690c900b870244cf25836515fc67895bc3092810ef89671c4f97ea`; locator `identity-proof:818003072`; method `signalpost.website.v1`.

<pre>			&lt;p&gt;Verksted og lager Lisbergvegen 9, 2740 Roa&lt;/p&gt;								&lt;/div&gt;
				&lt;/div&gt;
				&lt;div class="elementor-element elementor-element-080bdfe elementor-widget elementor-widget-heading" data-id="080bdfe" data-element_type="widget" data-e-type="widget" data-widget_type="heading.default"&gt;
				&lt;div class="e</pre>

### 825179062 - FTF CONSULTING AS - website

- url: `https://www.ftfconsulting.no`
- proof tier: `registry_declared_publisher_name`
- identity level: `HIGH`
- automated verdict: **doubtful** (No exact target orgnr in saved owner/proof context; published signal-only tier requires hand review; Published identity tier is below exact-number VERIFIED; Saved page proof needs review: corroboration)

Source: https://www.ftfconsulting.no/

Retrieved: 2026-11-16T08:34:00.707812Z; SHA-256 `b4c61a0d47e85bba09949b5418e74ce2ef20009e8f5af7ca65a0dd3fb78099ea`; locator `identity-proof:825179062`; method `signalpost.website.v1`.

<pre>-50"&gt;&lt;div class="container"&gt;Copyright © FTF Consulting AS 2020&lt;/div&gt;&lt;/footer&gt;
        &lt;!-- Bootstrap core JS--&gt;
        &lt;script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.4.1/jquery.min.js"&gt;&lt;/script&gt;
        &lt;script src="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.bundl</pre>

Source: https://www.ftfconsulting.no/

Retrieved: 2026-11-16T08:34:00.707812Z; SHA-256 `b4c61a0d47e85bba09949b5418e74ce2ef20009e8f5af7ca65a0dd3fb78099ea`; locator `registry-contact:email_domain`; method `signalpost.registry_contact.v1`.

<pre>&lt;a href="mailto:post@ftfconsulting.no"&gt;</pre>

### 911719266 - RESTAURANTDRIFT AS - website

- url: `https://restaurantdrift.no`
- proof tier: `publisher_name_rare_contact`
- identity level: `HIGH`
- automated verdict: **doubtful** (No exact target orgnr in saved owner/proof context; published signal-only tier requires hand review; Published identity tier is below exact-number VERIFIED; Saved page proof needs review: corroboration)

Source: https://restaurantdrift.no/

Retrieved: 2026-11-16T08:19:10.605872Z; SHA-256 `deb448d3b85ba00a9d1ec9df8138b0070916d92d75f195e4b76dff4ac45bdb93`; locator `identity-proof:911719266`; method `signalpost.website.v1`.

<pre>	&lt;/a&gt;
			&lt;/div&gt;
			
&lt;p class="mainText"&gt;Restaurantdrift AS har ett fundament fra hotell og restaurantdrift gjennom flere generasjoner innen virksomhet av Kafeer, restauranter, utleie av personell, konsulentbistand, catering, lagerhotell, kjøp/salg og import samt konsulentbistand fra Østen.&lt;/p&gt;

&lt;img</pre>

### 916094051 - BJØRNS BIL AS - website

- url: `https://www.bjornsbil.no`
- proof tier: `signals`
- identity level: `HIGH`
- automated verdict: **doubtful** (No exact target orgnr in saved owner/proof context; published signal-only tier requires hand review; Published identity tier is below exact-number VERIFIED; Saved page proof needs review: corroboration)

Source: https://www.bjornsbil.no/

Retrieved: 2026-11-16T08:38:01.687251Z; SHA-256 `fac518b5c8abf5e121780417329895d2333159a3a35df3cc76ee8d350b7557d6`; locator `identity-proof:916094051`; method `signalpost.website.v1`.

<pre>"https://www.bjornsbil.no/tenester/"&gt;Om Bj&amp;oslash;rns bil&lt;/a&gt;&lt;/li&gt;
&lt;li id="menu-item-13" class="menu-item menu-item-type-taxonomy menu-item-object-category menu-item-13"&gt;&lt;a href="https://www.bjornsbil.no/kontakt/"&gt;Kontakt&lt;/a&gt;&lt;/li&gt;
&lt;li id="menu-item-11" class="menu-item menu-item-type-taxonomy menu-i</pre>

Source: https://www.bjornsbil.no/

Retrieved: 2026-11-16T08:38:01.687251Z; SHA-256 `fac518b5c8abf5e121780417329895d2333159a3a35df3cc76ee8d350b7557d6`; locator `registry-contact:email_domain`; method `signalpost.registry_contact.v1`.

<pre>&lt;a href="mailto:post@bjornsbil.no"&gt;</pre>

### 918811370 - TOTEN FORSIKRING AS - website

- url: `https://totenforsikring.no`
- proof tier: `orgnr_on_page`
- identity level: `VERIFIED`
- automated verdict: **wrong** (StopIteration)

Source: https://totenforsikring.no/wp-content/uploads/2023/03/Angreskjema-Toten-2.pdf

Retrieved: 2026-11-16T08:27:52.570456Z; SHA-256 `5b3f3b24a0c229693c279133aad7fee2f165360228e082b3e79ddfe73ccf1133`; locator `pdf:page:1/identity-proof:918811370`; method `signalpost.website.v1`.

<pre>oten Forsikring AS
Organisasjonsnummer 
918811370  
Telefonnummer Adresse 
Jernbanesvingen 6, 2821 Gjøvik 990 13 282 
E-postadresse 
service@totenfors</pre>

Source: https://totenforsikring.no/wp-content/uploads/2023/03/Angreskjema-Toten-2.pdf

Retrieved: 2026-11-16T08:27:52.570456Z; SHA-256 `d0347d389a513abb5c91b1725f03df05e132d2db6638ebc6e8a486efc557bdd6`; locator `pdf:original`; method `signalpost.legal_pdf.v1`.

<pre>%PDF-</pre>

Source: https://totenforsikring.no/angrerett/

Retrieved: 2026-11-16T08:27:50.423327Z; SHA-256 `3eb9ede087a662a9022ff0eda91e219189b16fff277aac89518a1c2844c888ab`; locator `legal-pdf-link:https://totenforsikring.no/wp-content/uploads/2023/03/Angreskjema-Toten-2.pdf`; method `signalpost.legal_pdf.v1`.

<pre>&lt;a id="link_text-125-365" class="ct-link-text" href="https://totenforsikring.no/wp-content/uploads/2023/03/Angreskjema-Toten-2.pdf" target="_blank"  &gt;</pre>

### 922569738 - SNUOM PSYKISK HELSE AS - website

- url: `https://www.snuom.no`
- proof tier: `signals`
- identity level: `HIGH`
- automated verdict: **doubtful** (No exact target orgnr in saved owner/proof context; published signal-only tier requires hand review; Published identity tier is below exact-number VERIFIED; Saved page proof needs review: corroboration)

Source: https://www.snuom.no/

Retrieved: 2026-11-16T08:33:46.896503Z; SHA-256 `48ffa66134daa87df8d84032e137f3daca0d8f1ba8e064fce523db912a54fd49`; locator `identity-proof:922569738`; method `signalpost.website.v1`.

<pre>h2 class="font_2 wixui-rich-text__text"&gt;Snuom Psykisk Helse AS er en privat klinikk. Vi samarbeider tett med fastleger, forsikringsselskap og arbeidsgivere, og tilbyr rask oppstart uten henvisning eller ventetid i det offentlige systemet.&lt;/h2&gt;&lt;/div&gt;&lt;!--/$--&gt;&lt;/div&gt;&lt;!--/$--&gt;&lt;/div&gt;&lt;!--/$--&gt;&lt;/div&gt;&lt;/div&gt;</pre>

Source: https://www.snuom.no/

Retrieved: 2026-11-16T08:33:46.896503Z; SHA-256 `48ffa66134daa87df8d84032e137f3daca0d8f1ba8e064fce523db912a54fd49`; locator `registry-contact:phone`; method `signalpost.registry_contact.v1`.

<pre>&lt;a data-testid="linkElement" href="tel:+47 74 38 85 00" class="PoVCDy wixui-button ZhVEJq" aria-disabled="false" aria-label="Ring oss"&gt;</pre>

Source: https://www.snuom.no/

Retrieved: 2026-11-16T08:33:46.896503Z; SHA-256 `48ffa66134daa87df8d84032e137f3daca0d8f1ba8e064fce523db912a54fd49`; locator `registry-contact:email_domain`; method `signalpost.registry_contact.v1`.

<pre>&lt;a href="mailto:post@snuom.no?subject=Book time" target="_self" class="wixui-rich-text__text"&gt;</pre>

### 925193313 - UNDERVISNINGSMATERIELL AS - website

- url: `https://undervisningsmateriell.no`
- proof tier: `publisher_name_rare_contact`
- identity level: `HIGH`
- automated verdict: **doubtful** (No exact target orgnr in saved owner/proof context; published signal-only tier requires hand review; Published identity tier is below exact-number VERIFIED; Saved page proof needs review: corroboration)

Source: https://undervisningsmateriell.no/

Retrieved: 2026-11-16T08:33:54.790372Z; SHA-256 `c1b98683e51fabd9462dce24656a44c8773eb7459912aaa892e519c0193c0133`; locator `identity-proof:925193313`; method `signalpost.website.v1`.

<pre>set="windows-1252"&gt;
&lt;title&gt;Nettbutikk - Undervisningsmateriell AS&lt;/title&gt;
&lt;meta name="viewport" content="width=device-width, initial-scale=1"&gt;
&lt;meta name="generator" content="SmartWeb"&gt;
&lt;meta name="csrf_token" content="MTc5NDgxODAzM2VhZTlkOTk2MjI2YjA0NDJiODAxNDY4YTdhZGQ4OGIyNjgwNzhiMzBJeER6NVdSbHFle</pre>

Source: https://undervisningsmateriell.no/

Retrieved: 2026-11-16T08:33:54.790372Z; SHA-256 `c1b98683e51fabd9462dce24656a44c8773eb7459912aaa892e519c0193c0133`; locator `registry-contact:phone`; method `signalpost.registry_contact.v1`.

<pre>&lt;a href="tel:22 70 00 10"&gt;</pre>

Source: https://undervisningsmateriell.no/

Retrieved: 2026-11-16T08:33:54.790372Z; SHA-256 `c1b98683e51fabd9462dce24656a44c8773eb7459912aaa892e519c0193c0133`; locator `registry-contact:email_domain`; method `signalpost.registry_contact.v1`.

<pre>&lt;a href="mailto:post@undervisningsmateriell.no"&gt;</pre>

### 929455606 - INDUSTRIPLAST AS - website

- url: `https://industriplast.no`
- proof tier: `publisher_name_registered_place`
- identity level: `HIGH`
- automated verdict: **doubtful** (No exact target orgnr in saved owner/proof context; published signal-only tier requires hand review; Published identity tier is below exact-number VERIFIED; Saved page proof needs review: corroboration)

Source: https://industriplast.no/

Retrieved: 2026-11-16T08:38:27.177436Z; SHA-256 `ca330b3711e0a6a1509184fc2a740a9c8caa0c731b0ab661aa2e7181729b5e49`; locator `identity-proof:929455606`; method `signalpost.website.v1`.

<pre>ment " &gt;
	&lt;h1 class="overskriftforside"&gt;Industriplast AS:&lt;/h1&gt;
&lt;h2&gt;Kvalitet &amp;amp; kunnskap siden 1963&lt;/h2&gt;
&lt;h1&gt;&lt;span style="color: #e38d31;"&gt;Produksjon av&lt;/span&gt;&lt;br /&gt;
&lt;span style="color: #e38d31;"&gt;rør, plastprofiler&lt;/span&gt;&lt;br /&gt;
&lt;span style="color: #e38d31;"&gt;&amp;amp; slanger&lt;/span&gt;&lt;/h1&gt;
&lt;/div&gt;




		&lt;</pre>

### 956510651 - KIRKENG EIENDOM AS - website

- url: `https://kirkengeiendom.no`
- proof tier: `publisher_name_registered_place`
- identity level: `HIGH`
- automated verdict: **doubtful** (No exact target orgnr in saved owner/proof context; published signal-only tier requires hand review; Published identity tier is below exact-number VERIFIED; Saved page proof needs review: corroboration)

Source: https://kirkengeiendom.no/kontakt-oss/

Retrieved: 2026-11-16T08:30:18.995696Z; SHA-256 `6003c0b6c5f0aa6915eb5429607ce5c48def9d22c4078aecd29e5035a3cbccaa`; locator `identity-proof:956510651`; method `signalpost.website.v1`.

<pre>&lt;/div&gt;
	
&lt;p style="text-align: center;"&gt;Kirkeng Eiendom AS er for tiden fire heltidsansatte med følgende kontaktdetaljer:&lt;/p&gt;
&lt;p style="text-align: center;"&gt;Besøksadresse: Nedre Storgate 35, 3015 Drammen&lt;/p&gt;
&lt;p style="text-align: center;"&gt;Postboks 413, 3002 Drammen&lt;/p&gt;
		&lt;/div&gt;
			&lt;/div&gt;

	
&lt;/div&gt;
&lt;</pre>

### 989952625 - VARMEPUMPESERVICE AS - website

- url: `https://www.varmepumpeservice.no`
- proof tier: `signals`
- identity level: `HIGH`
- automated verdict: **doubtful** (No exact target orgnr in saved owner/proof context; published signal-only tier requires hand review; Published identity tier is below exact-number VERIFIED; Saved page proof needs review: corroboration)

Source: https://www.varmepumpeservice.no/

Retrieved: 2026-11-16T08:33:12.404231Z; SHA-256 `b52e6240266fc1017daf6a45f258c2541ea2e1004b68ea8a07d9cf79182aa83a`; locator `identity-proof:989952625`; method `signalpost.website.v1`.

<pre>
&lt;title&gt;Varmepumper | Bedre inneklima | Varmepumpeservice &lt;/title&gt;
&lt;meta name="generator" content="Gurusoft Ecommerce"&gt;
&lt;meta name="viewport" content="width=device-width, initial-scale=1.0"&gt;
&lt;meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/&gt;
&lt;meta http-equiv="X-UA-Compatible" conte</pre>

Source: https://www.varmepumpeservice.no/

Retrieved: 2026-11-16T08:33:12.404231Z; SHA-256 `b52e6240266fc1017daf6a45f258c2541ea2e1004b68ea8a07d9cf79182aa83a`; locator `registry-contact:email_domain`; method `signalpost.registry_contact.v1`.

<pre>&lt;a href="mailto:firmapost@varmepumpeservice.no"&gt;</pre>

### 991380523 - KVERNODDEN AS - website

- url: `https://kvernodden.no`
- proof tier: `registry_declared_publisher_name`
- identity level: `HIGH`
- automated verdict: **doubtful** (No exact target orgnr in saved owner/proof context; published signal-only tier requires hand review; Published identity tier is below exact-number VERIFIED; Saved page proof needs review: corroboration)

Source: https://kvernodden.no/

Retrieved: 2026-11-16T08:18:56.952457Z; SHA-256 `bbf255c4a3720e763afca7514ff2d88dbbb11e44d78ccbcd9075d7f536fbe3fd`; locator `identity-proof:991380523`; method `signalpost.website.v1`.

<pre>             &lt;p class="u-text u-text-6"&gt;Kvernodden AS&lt;br&gt;Kjeldalsvegen 42&lt;br&gt;3825 LUNDE&lt;br&gt;
                  &lt;br&gt;
                &lt;/p&gt;
              &lt;/div&gt;
            &lt;/div&gt;
            &lt;div class="u-align-left u-container-align-left u-container-style u-image u-layout-cell u-size-20-lg u-size-20-m</pre>

### 992912952 - DOVRE HANDVERK AS - website

- url: `https://www.dovrehandverk.no`
- proof tier: `registry_declared_live`
- identity level: `HIGH`
- automated verdict: **doubtful** (No exact target orgnr in saved owner/proof context; published signal-only tier requires hand review; Published identity tier is below exact-number VERIFIED; Saved page proof needs review: corroboration)

Source: https://www.dovrehandverk.no/

Retrieved: 2026-11-16T08:20:45.305420Z; SHA-256 `436f6c90b32a19318cfe346446c669a2e7da9ba16a82d074f50dfc8278dc2f19`; locator `identity-proof:992912952`; method `signalpost.website.v1`.

<pre>unk.min.css.map*/&lt;/style&gt;
&lt;title&gt;Home | Dovre Handverk&lt;/title&gt;
  &lt;link rel="canonical" href="https://www.dovrehandverk.no"/&gt;
  &lt;meta property="og:title" content="Home | Dovre Handverk"/&gt;
  &lt;meta property="og:url" content="https://www.dovrehandverk.no"/&gt;
  &lt;meta property="og:site_name" content="Dovre</pre>

### 996441083 - KVITSØY SJØTJENESTER AS - website

- url: `https://www.seaservices.no`
- proof tier: `signals`
- identity level: `HIGH`
- automated verdict: **doubtful** (No exact target orgnr in saved owner/proof context; published signal-only tier requires hand review; Published identity tier is below exact-number VERIFIED; Saved page proof needs review: corroboration)

Source: https://www.seaservices.no/

Retrieved: 2026-11-16T08:23:48.352461Z; SHA-256 `cbdbbffb09321767d5fd712666aecc58628c5272d60a8e9af75d95cac4ec7b0d`; locator `identity-proof:996441083`; method `signalpost.website.v1`.

<pre>a333.chunk.min.css.map*/&lt;/style&gt;
&lt;title&gt;Kvitsøy Sjøtjenester – Frakt, transport og miljø&lt;/title&gt;
  &lt;meta name="description" content="Kvitsøy Sjøtjenester leverer frakt, transport av rensefisk, personer og varer, miljøovervåking og berging langs kysten. "/&gt;
  &lt;link rel="canonical" href="https://www.s</pre>

Source: https://www.seaservices.no/

Retrieved: 2026-11-16T08:23:48.352461Z; SHA-256 `cbdbbffb09321767d5fd712666aecc58628c5272d60a8e9af75d95cac4ec7b0d`; locator `registry-contact:email_domain`; method `signalpost.registry_contact.v1`.

<pre>&lt;a data-auto-recognition="true" href="mailto:post@seaservices.no" class="wixui-rich-text__text"&gt;</pre>

## Website — automated correct (23)

### 827458392 - SMARTE HODER AS - website

- url: `https://www.smarte-hoder.no`
- proof tier: `orgnr_on_page`
- identity level: `VERIFIED`
- automated verdict: **correct**

Source: https://www.smarte-hoder.no/

Retrieved: 2026-11-16T08:24:30.669891Z; SHA-256 `aca2eb1b2737edc724ffd709df5cc892b95754e8072479c1bd687a8057b9035e`; locator `identity-proof:827458392`; method `signalpost.website.v1`.

<pre>er" style="text-decoration: underline;"&gt;827 458 392&lt;/a&gt;&lt;/span&gt; &lt;br /&gt;&lt;a href="https://www.smarte-hoder.no/personvern/"&gt;&lt;span style="text-decoration: u</pre>

### 835090442 - HJEMVENT AS - website

- url: `https://www.hjemvent.no`
- proof tier: `orgnr_on_page`
- identity level: `VERIFIED`
- automated verdict: **correct**

Source: https://www.hjemvent.no/

Retrieved: 2026-11-16T08:32:41.801236Z; SHA-256 `b4df5f6f65780abec4cb77dacc7bd0ba9c4324faad8cf2b800284ba9b16c44cc`; locator `identity-proof:835090442`; method `signalpost.website.v1`.

<pre>o"&gt;kontakt@hjemvent.no&lt;/a&gt;&lt;br /&gt;
Org.no 835090442&lt;/p&gt;
&lt;/div&gt;
		&lt;/div&gt;&lt;div id="custom_html-9" class="widget_text widget widget_custom_html"&gt;&lt;span class</pre>

### 915448984 - DEATHTRAP CUSTOMS AS - website

- url: `https://deathtrap-customs.com`
- proof tier: `jsonld_vatid`
- identity level: `VERIFIED`
- automated verdict: **correct**

Source: https://deathtrap-customs.com/

Retrieved: 2026-11-16T08:34:05.115830Z; SHA-256 `013f88db1ee47cc86a905a5ae2e949a1302c6f0bc9c444b4d098d552bbaa20ae`; locator `identity-proof:915448984`; method `signalpost.website.v1`.

<pre>6609"&gt;64946609&lt;/a&gt; - Foretaksregisteret 915 448 984 MVA&lt;/div&gt;        &lt;/div&gt;

        &lt;div class="columns small-12"&gt;
            &lt;div class="text-align</pre>

Source: https://deathtrap-customs.com/

Retrieved: 2026-11-16T08:34:05.115830Z; SHA-256 `013f88db1ee47cc86a905a5ae2e949a1302c6f0bc9c444b4d098d552bbaa20ae`; locator `registry-contact:phone`; method `signalpost.registry_contact.v1`.

<pre>&lt;a href="tel:64946609"&gt;</pre>

Source: https://deathtrap-customs.com/

Retrieved: 2026-11-16T08:34:05.115830Z; SHA-256 `013f88db1ee47cc86a905a5ae2e949a1302c6f0bc9c444b4d098d552bbaa20ae`; locator `registry-contact:email_domain`; method `signalpost.registry_contact.v1`.

<pre>":"Ski","addressCountry":"NO"},"email":"shop@deathtrap-customs.com","telephone":"64946609","identifier":"915 448 984 MVA"}&lt;/script&gt;&lt;script type="application/ld+json"&gt;{"@context":"https://schema.org","@type":"WebSite","@id":"https://deathtrap-customs.com/#website","url":"https://deathtrap-customs.com</pre>

### 919257121 - DICTION AS - website

- url: `https://www.diction.no`
- proof tier: `orgnr_on_page`
- identity level: `VERIFIED`
- automated verdict: **correct**

Source: https://www.diction.no/

Retrieved: 2026-11-16T08:33:00.875219Z; SHA-256 `6915e1f8ef7270f4dfe834611aa76da89263bf3bca1ab238a450fec4e835e4fc`; locator `identity-proof:919257121`; method `signalpost.website.v1`.

<pre>an&gt;&lt;/a&gt;&lt;/div&gt;&lt;div class="mt-6"&gt;Org.nr.: 919 257 121&lt;/div&gt;&lt;div class="mt-2"&gt;EAN: 5797200064202&lt;/div&gt;&lt;div class="mt-6 flex"&gt;&lt;a target="_blank" href="htt</pre>

### 919825839 - NORSKE VILLSAUSKINN AS - website

- url: `https://norskevillsauskinn.no`
- proof tier: `orgnr_on_page`
- identity level: `VERIFIED`
- automated verdict: **correct**

Source: https://norskevillsauskinn.no/

Retrieved: 2026-11-16T08:25:44.491096Z; SHA-256 `121eca9142683cda700bc90aca6e46d93b5015631ae096d3f70f02a66b6481e4`; locator `identity-proof:919825839`; method `signalpost.website.v1`.

<pre>n 901&lt;br /&gt;
4580 Lyngdal&lt;br /&gt;
Org. nr: 919 825 839&lt;/p&gt;
&lt;p&gt;Tlf: &lt;a href="tel:004792087642"&gt;920 87 642&lt;/a&gt;&lt;/p&gt;
&lt;p&gt;&amp;nbsp;&lt;/p&gt;
&lt;/div&gt;
		&lt;/div&gt;&lt;/div&gt;&lt;div </pre>

### 921253125 - PARKSIDE1 AS - website

- url: `https://www.parkside.no`
- proof tier: `orgnr_on_page`
- identity level: `VERIFIED`
- automated verdict: **correct**

Source: https://www.parkside.no/

Retrieved: 2026-11-16T08:32:36.084912Z; SHA-256 `7988c02c9a117af8d0d8e2984e93922638216321a5fb565cccc0b64375c4a6ff`; locator `identity-proof:921253125`; method `signalpost.website.v1`.

<pre>contact-item-value"&gt;Parkside1 AS · Org. 921 253 125&lt;/span&gt;
          &lt;/div&gt;
        &lt;/div&gt;
      &lt;/div&gt;
    &lt;/div&gt;
  &lt;/section&gt;

  &lt;!-- ── FOOTER ────</pre>

Source: https://www.parkside.no/

Retrieved: 2026-11-16T08:32:36.084912Z; SHA-256 `7988c02c9a117af8d0d8e2984e93922638216321a5fb565cccc0b64375c4a6ff`; locator `registry-contact:email_domain`; method `signalpost.registry_contact.v1`.

<pre>&lt;a href="mailto:post@parkside.no" class="contact-item-value"&gt;</pre>

### 922128693 - GULCON AS - website

- url: `https://gulcon.no`
- proof tier: `orgnr_on_page`
- identity level: `VERIFIED`
- automated verdict: **correct**

Source: https://gulcon.no/

Retrieved: 2026-11-16T08:20:12.499738Z; SHA-256 `1d886b06e2fc2b5ca1e6616c5ffa809fa7b4808a699f41a3b058635d875d03ee`; locator `identity-proof:922128693`; method `signalpost.website.v1`.

<pre> &lt;/p&gt;&lt;p class="wb-stl-custom11"&gt;Orgnr.: 922128693&lt;br&gt;&lt;/p&gt;&lt;p class="wb-stl-custom10" style="text-align:center;"&gt; &lt;a href="" title=""&gt;K&lt;/a&gt;ONTAKTINFORMA</pre>

### 924487437 - IRONSTEEL SCANDINAVIA AS - website

- url: `https://www.ironsteelscandinavia.com`
- proof tier: `orgnr_on_page`
- identity level: `VERIFIED`
- automated verdict: **correct**

Source: https://www.ironsteelscandinavia.com/

Retrieved: 2026-11-16T08:36:39.029144Z; SHA-256 `0cdd9f86faeafe3ce1fe6f36afd3af90ee94b9c791dd032def46db8f68750290`; locator `identity-proof:924487437`; method `signalpost.website.v1`.

<pre>26 | Ironsteel Scandinavia AS | Org.no: 924 487 437 | E-mail: post@ironsteelscandinavia.com&lt;/span&gt;
                        &lt;span class="copyright__by</pre>

### 924949341 - CURATED BRANDS AS - website

- url: `https://goodnotes.no`
- proof tier: `orgnr_on_page`
- identity level: `VERIFIED`
- automated verdict: **correct**

Source: https://goodnotes.no/

Retrieved: 2026-11-16T08:19:48.255504Z; SHA-256 `40dc734dbff1a20a46453c729ae194c0974ea25ce840acf3b6e9baacb8400d12`; locator `identity-proof:924949341`; method `signalpost.website.v1`.

<pre>r__company"&gt;Curated Brands AS · Org.nr. 924 949 341&lt;/span&gt;&lt;/small&gt;
      &lt;/div&gt;

      &lt;ul role="list"&gt;
        
          
            
             </pre>

### 927361426 - L TERRASSE AS - website

- url: `https://lterrasse.no`
- proof tier: `orgnr_on_page`
- identity level: `VERIFIED`
- automated verdict: **correct**

Source: https://lterrasse.no/

Retrieved: 2026-11-16T08:36:57.115731Z; SHA-256 `fb2f834560b9477a2392e9e0232b3a884f6ab0c4c48309c5869b46881ccd60c1`; locator `identity-proof:927361426`; method `signalpost.website.v1`.

<pre>gen 10&lt;br /&gt;
7900 RØRVIK&lt;br /&gt;
Org. nr. 927 361 426&lt;/p&gt;
&lt;/div&gt;
		&lt;/div&gt;				&lt;/div&gt;
			
					&lt;/div&gt;
	&lt;/div&gt;
&lt;/footer&gt;
		
		
&lt;div id="bottom" clas</pre>

### 928179273 - ARNHEIM AS - website

- url: `https://arnheim.no`
- proof tier: `jsonld_vatid`
- identity level: `VERIFIED`
- automated verdict: **correct**

Source: https://arnheim.no/

Retrieved: 2026-11-16T08:22:42.896070Z; SHA-256 `4ce7315aabfea7d67585694bc4829f2eda6441dd4368c9cc4906e0b595c2f651`; locator `identity-proof:928179273`; method `signalpost.website.v1`.

<pre>        &lt;dd class="datasheet__val mono"&gt;928 179 273&lt;/dd&gt;
            &lt;/div&gt;
            &lt;div class="datasheet__row"&gt;
              &lt;dt class="datashee</pre>

### 928507289 - BORITA AS - website

- url: `https://borita.no`
- proof tier: `orgnr_on_page`
- identity level: `VERIFIED`
- automated verdict: **correct**

Source: https://borita.no/

Retrieved: 2026-11-16T08:35:46.378984Z; SHA-256 `07abc4238bfc087911000602743d095a81b6036a8a3ff9d5ac9994b02595898d`; locator `identity-proof:928507289`; method `signalpost.website.v1`.

<pre>ta.no"&gt;rita@borita.no&lt;/a&gt;&lt;br&gt;• Org. nr: 928 50 7289&lt;/p&gt;
&lt;/div&gt;&lt;div id="block-11" class="fwidget et_pb_widget widget_block widget_text"&gt;
&lt;p class="wp-b</pre>

### 928593886 - FLORENTES DESIGN AS - website

- url: `https://florentesdesign.no`
- proof tier: `jsonld_vatid`
- identity level: `VERIFIED`
- automated verdict: **correct**

Source: https://florentesdesign.no/

Retrieved: 2026-11-16T08:36:54.761364Z; SHA-256 `b9970fd2e0082fefd48aadd2124fab582ad398338317a09ea4b319be573d3888`; locator `identity-proof:928593886`; method `signalpost.website.v1`.

<pre>                                    &lt;dd&gt;928593886&lt;/dd&gt;
                                &lt;/dl&gt;
                                
                        </pre>

### 931340476 - GINNTECH AS - website

- url: `https://ginntech.com`
- proof tier: `orgnr_on_page`
- identity level: `VERIFIED`
- automated verdict: **correct**

Source: https://ginntech.com/nb

Retrieved: 2026-11-16T08:33:27.039641Z; SHA-256 `60131a9f6b70eb88e1abe2f9b17baae58d47a420791b61fcc5b5c155b6d1f860`; locator `identity-proof:931340476`; method `signalpost.website.v1`.

<pre>ong field--label-hidden field__item"&gt;&lt;p&gt;931340476 MVA&lt;/p&gt;
&lt;/div&gt;
            
  &lt;/div&gt;

    &lt;/div&gt;
  &lt;/div&gt;

  &lt;/div&gt;

            &lt;/div&gt;
            </pre>

### 932296047 - KURVE REGNSKAP AS - website

- url: `https://kurveregnskap.no`
- proof tier: `orgnr_on_page`
- identity level: `VERIFIED`
- automated verdict: **correct**

Source: https://kurveregnskap.no/

Retrieved: 2026-11-16T08:30:08.489270Z; SHA-256 `de08b920895bcc6491ad922ef4accc8b6f05d0d63bf14cfafdc468f488c0ba63`; locator `identity-proof:932296047`; method `signalpost.website.v1`.

<pre>egnskap.no&lt;/a&gt;&lt;br&gt;
            Org.nr.: 932296047&lt;br&gt;
            &lt;img decoding="async" src="https://kurveregnskap.no/wp-content/uploads/2025/06/diama</pre>

### 933831922 - SHIFT SECURITY AS - website

- url: `https://shiftsecurity.no`
- proof tier: `orgnr_on_page`
- identity level: `VERIFIED`
- automated verdict: **correct**

Source: https://shiftsecurity.no/personvernerklaring

Retrieved: 2026-11-16T08:31:28.536856Z; SHA-256 `fe56c5e23d3778e10d3c0b193e242a2799f3a57b8262808e022be4fb2822ab72`; locator `identity-proof:933831922`; method `signalpost.website.v1`.

<pre>ift Security AS&lt;br&gt;Organisasjonsnummer: 933 831 922&lt;br&gt;E-post: &lt;a href="mailto:post@shiftsecurity.no" rel="noopener"&gt;post@shiftsecurity.no&lt;/a&gt;&lt;/span&gt;&lt;</pre>

### 948501341 - HARALDSEID ELEKTRISKE AS - website

- url: `https://www.haraldseid-elektriske.no`
- proof tier: `orgnr_on_page`
- identity level: `VERIFIED`
- automated verdict: **correct**

Source: https://www.haraldseid-elektriske.no/

Retrieved: 2026-11-16T08:30:35.409705Z; SHA-256 `725926782edf46ae32f289bac2944bf086a1730fcc09d510ad8edb0036c9c327`; locator `identity-proof:948501341`; method `signalpost.website.v1`.

<pre>mber"&gt;
                        Org.no.: 948501341
                    &lt;/div&gt;
                            &lt;/div&gt;

            

                       </pre>

### 971050756 - ACCELLA SOLUTIONS AS - website

- url: `https://accella.no`
- proof tier: `orgnr_on_page`
- identity level: `VERIFIED`
- automated verdict: **correct**

Source: https://accella.no/

Retrieved: 2026-11-16T08:35:41.607895Z; SHA-256 `29222d28f69806a90fffe46bb802ecb081987fe6a988e695aea32e2331449573`; locator `identity-proof:971050756`; method `signalpost.website.v1`.

<pre>ass="elementor-icon-list-text"&gt;Org.nr.: 971.050.756&lt;/span&gt;
									&lt;/li&gt;
						&lt;/ul&gt;
						&lt;/div&gt;
				&lt;/div&gt;
					&lt;/div&gt;
		&lt;/div&gt;
				&lt;div class="ele</pre>

Source: https://accella.no/

Retrieved: 2026-11-16T08:35:41.607895Z; SHA-256 `29222d28f69806a90fffe46bb802ecb081987fe6a988e695aea32e2331449573`; locator `registry-contact:phone`; method `signalpost.registry_contact.v1`.

<pre>&lt;a href="tel:+4723060340"&gt;</pre>

### 971076526 - VVS RØRLEGGER AS - website

- url: `https://www.vvsrorlegger.no`
- proof tier: `orgnr_on_page`
- identity level: `VERIFIED`
- automated verdict: **correct**

Source: https://www.vvsrorlegger.no/

Retrieved: 2026-11-16T08:35:04.176519Z; SHA-256 `3dece77b3e9545e4226ae23ff78529a78aab1659f926db409556a62d70bfa25a`; locator `identity-proof:971076526`; method `signalpost.website.v1`.

<pre>sp;Godøyvegen 2, 6055 Godøya&lt;br&gt;Org.nr: 971 076 526&lt;/p&gt;&lt;/div&gt; &lt;/div&gt; &lt;div id="c3299" class="col col-sm-12 col-md-5 palette_bc_#076472 col-lg-4"&gt;&lt;div i</pre>

Source: https://www.vvsrorlegger.no/

Retrieved: 2026-11-16T08:35:04.176519Z; SHA-256 `3dece77b3e9545e4226ae23ff78529a78aab1659f926db409556a62d70bfa25a`; locator `registry-contact:phone`; method `signalpost.registry_contact.v1`.

<pre>&lt;a data-global="phone"  href="tel:99509816" data-track-event="click" data-track-action="phone_link"&gt;</pre>

### 977485576 - MASKINKRAFT AS - website

- url: `https://www.maskinkraft.no`
- proof tier: `orgnr_on_page`
- identity level: `VERIFIED`
- automated verdict: **correct**

Source: https://www.maskinkraft.no/

Retrieved: 2026-11-16T08:20:58.248774Z; SHA-256 `1e6339ce7c846cb8272cbef8a2cd66fe1fbacb0551f95f49945b61cd0ba44c66`; locator `identity-proof:977485576`; method `signalpost.website.v1`.

<pre>k_clicked"&gt;&lt;span class="monoglobalWrap"&gt;977 485 576&lt;/span&gt;&lt;/a&gt;&lt;/p&gt;&lt;/div&gt; &lt;div id="m3485" class="module text"&gt;&lt;h4 class="smallsubtitle"&gt;Åpningstider&lt;/h</pre>

### 981390350 - GRENDA AS - website

- url: `https://www.grenda.no`
- proof tier: `orgnr_on_page`
- identity level: `VERIFIED`
- automated verdict: **correct**

Source: https://www.grenda.no/vilkar

Retrieved: 2026-11-16T08:25:49.675242Z; SHA-256 `e00596feccb7a7b0d2ed82c001221b0288cd37675c86404699df8535247e42d2`; locator `identity-proof:981390350`; method `signalpost.website.v1`.

<pre>elefon: 53 48 71 00 &lt;br&gt;Foretaksreg: NO 981 390 350 MVA &lt;br&gt;E-post: &lt;a href="mailto:kundeservice@grenda.no" style="font-size: 1.125rem;"&gt;kundeservice@</pre>

Source: https://www.grenda.no/vilkar

Retrieved: 2026-11-16T08:25:49.675242Z; SHA-256 `e00596feccb7a7b0d2ed82c001221b0288cd37675c86404699df8535247e42d2`; locator `registry-contact:email_domain`; method `signalpost.registry_contact.v1`.

<pre>&lt;a href="mailto:kundeservice@grenda.no" style="font-size: 1.125rem;"&gt;</pre>

Source: https://www.grenda.no/vilkar

Retrieved: 2026-11-16T08:25:49.675242Z; SHA-256 `e00596feccb7a7b0d2ed82c001221b0288cd37675c86404699df8535247e42d2`; locator `registry-contact:phone`; method `signalpost.registry_contact.v1`.

<pre>ks 100&lt;br&gt;5486 Rosendal &lt;/p&gt;&lt;p&gt;Telefon: 53 48 71 00 &lt;br&gt;Foretaksreg: NO 981 390 350 MVA &lt;br&gt;E-post: &lt;a href="mailto:kundeservice@grenda.no" style="font-size: 1.125rem;"&gt;kundeservice@grenda.no&lt;/a&gt; &lt;br&gt;&lt;a href="https://www.grenda.no/" target="_blank"&gt;www.grenda.no&lt;/a&gt; &lt;br&gt;Bankkontonummer: 26600705090&lt;</pre>

### 987470305 - FLORØ BYGG AS - website

- url: `https://florobygg.no`
- proof tier: `orgnr_on_page`
- identity level: `VERIFIED`
- automated verdict: **correct**

Source: https://florobygg.no/

Retrieved: 2026-11-16T08:34:32.229499Z; SHA-256 `ddfc23a5574cc31fbc3b09102496494c79e348031012ff6ab6cb313ef0351d95`; locator `identity-proof:987470305`; method `signalpost.website.v1`.

<pre>/sok/detalj.jsp?orgnr=987470305"&gt;Orgnr: 987 470 305&lt;/a&gt;&lt;/p&gt;
&lt;p&gt;Evjegata 10, 6900 FLORØ&lt;/p&gt;
&lt;p&gt;T: &lt;a href="tel:5774770"&gt;57 74 77 00&lt;/a&gt;&lt;/p&gt;
&lt;/div&gt;&lt;/div</pre>

Source: https://florobygg.no/

Retrieved: 2026-11-16T08:34:32.229499Z; SHA-256 `ddfc23a5574cc31fbc3b09102496494c79e348031012ff6ab6cb313ef0351d95`; locator `registry-contact:phone`; method `signalpost.registry_contact.v1`.

<pre>&lt;a href="tel:57747700"&gt;</pre>

### 997103513 - GLOBAL CORPORATION AS - website

- url: `https://global-mac.no`
- proof tier: `orgnr_on_page`
- identity level: `VERIFIED`
- automated verdict: **correct**

Source: https://global-mac.no/

Retrieved: 2026-11-16T08:39:08.589181Z; SHA-256 `f77d50e9860dbd9fb56a3f239bb8d4b820cd9f91defd7858e48c97d0848c0f31`; locator `identity-proof:997103513`; method `signalpost.website.v1`.

<pre>&gt;©2026, Global Corporation AS / Org.nr: 997 103 513&lt;/span&gt;
          &lt;span class="mob-text"&gt;©2026, Global Corporation AS / Org.nr: 997 103 513&lt;/span&gt;
</pre>

## Social — automated correct (10)

### 827458392 - SMARTE HODER AS - social

- url: `https://www.instagram.com/smartehoderas`
- proof tier: `own_header_footer_exact_name_v1`
- automated verdict: **correct**

Source: https://www.smarte-hoder.no/

Retrieved: 2026-11-16T08:24:30.669891Z; SHA-256 `aca2eb1b2737edc724ffd709df5cc892b95754e8072479c1bd687a8057b9035e`; locator `company-link:https://www.instagram.com/smartehoderas`; method `signalpost.website.v1`.

<pre>&lt;a class="" href="https://www.instagram.com/smartehoderas/" target="_blank" rel="noopener" &gt;</pre>

Source: https://www.smarte-hoder.no/

Retrieved: 2026-11-16T08:24:30.669891Z; SHA-256 `aca2eb1b2737edc724ffd709df5cc892b95754e8072479c1bd687a8057b9035e`; locator `identity-proof:827458392`; method `signalpost.website.v1`.

<pre>er" style="text-decoration: underline;"&gt;827 458 392&lt;/a&gt;&lt;/span&gt; &lt;br /&gt;&lt;a href="https://www.smarte-hoder.no/personvern/"&gt;&lt;span style="text-decoration: u</pre>

### 827458392 - SMARTE HODER AS - social

- url: `https://www.linkedin.com/company/smarte-hoder-as`
- proof tier: `own_header_footer_exact_name_v1`
- automated verdict: **correct**

Source: https://www.smarte-hoder.no/

Retrieved: 2026-11-16T08:24:30.669891Z; SHA-256 `aca2eb1b2737edc724ffd709df5cc892b95754e8072479c1bd687a8057b9035e`; locator `company-link:https://www.linkedin.com/company/smarte-hoder-as`; method `signalpost.website.v1`.

<pre>&lt;a class="" href="https://www.linkedin.com/company/smarte-hoder-as/?viewAsMember=true" target="_blank" rel="noopener" &gt;</pre>

Source: https://www.smarte-hoder.no/

Retrieved: 2026-11-16T08:24:30.669891Z; SHA-256 `aca2eb1b2737edc724ffd709df5cc892b95754e8072479c1bd687a8057b9035e`; locator `identity-proof:827458392`; method `signalpost.website.v1`.

<pre>er" style="text-decoration: underline;"&gt;827 458 392&lt;/a&gt;&lt;/span&gt; &lt;br /&gt;&lt;a href="https://www.smarte-hoder.no/personvern/"&gt;&lt;span style="text-decoration: u</pre>

### 919825839 - NORSKE VILLSAUSKINN AS - social

- url: `https://www.facebook.com/norskevillsauskinn`
- proof tier: `own_header_footer_exact_name_v1`
- automated verdict: **correct**

Source: https://norskevillsauskinn.no/

Retrieved: 2026-11-16T08:25:44.491096Z; SHA-256 `121eca9142683cda700bc90aca6e46d93b5015631ae096d3f70f02a66b6481e4`; locator `company-link:https://www.facebook.com/norskevillsauskinn`; method `signalpost.website.v1`.

<pre>&lt;a href="https://www.facebook.com/norskevillsauskinn/" class="icon"&gt;</pre>

Source: https://norskevillsauskinn.no/

Retrieved: 2026-11-16T08:25:44.491096Z; SHA-256 `121eca9142683cda700bc90aca6e46d93b5015631ae096d3f70f02a66b6481e4`; locator `identity-proof:919825839`; method `signalpost.website.v1`.

<pre>n 901&lt;br /&gt;
4580 Lyngdal&lt;br /&gt;
Org. nr: 919 825 839&lt;/p&gt;
&lt;p&gt;Tlf: &lt;a href="tel:004792087642"&gt;920 87 642&lt;/a&gt;&lt;/p&gt;
&lt;p&gt;&amp;nbsp;&lt;/p&gt;
&lt;/div&gt;
		&lt;/div&gt;&lt;/div&gt;&lt;div </pre>

### 919825839 - NORSKE VILLSAUSKINN AS - social

- url: `https://www.instagram.com/norskevillsauskinn`
- proof tier: `own_header_footer_exact_name_v1`
- automated verdict: **correct**

Source: https://norskevillsauskinn.no/

Retrieved: 2026-11-16T08:25:44.491096Z; SHA-256 `121eca9142683cda700bc90aca6e46d93b5015631ae096d3f70f02a66b6481e4`; locator `company-link:https://www.instagram.com/norskevillsauskinn`; method `signalpost.website.v1`.

<pre>&lt;a href="https://www.instagram.com/norskevillsauskinn/" class="icon"&gt;</pre>

Source: https://norskevillsauskinn.no/

Retrieved: 2026-11-16T08:25:44.491096Z; SHA-256 `121eca9142683cda700bc90aca6e46d93b5015631ae096d3f70f02a66b6481e4`; locator `identity-proof:919825839`; method `signalpost.website.v1`.

<pre>n 901&lt;br /&gt;
4580 Lyngdal&lt;br /&gt;
Org. nr: 919 825 839&lt;/p&gt;
&lt;p&gt;Tlf: &lt;a href="tel:004792087642"&gt;920 87 642&lt;/a&gt;&lt;/p&gt;
&lt;p&gt;&amp;nbsp;&lt;/p&gt;
&lt;/div&gt;
		&lt;/div&gt;&lt;/div&gt;&lt;div </pre>

### 931340476 - GINNTECH AS - social

- url: `https://www.linkedin.com/company/ginntech`
- proof tier: `own_header_footer_exact_name_v1`
- automated verdict: **correct**

Source: https://ginntech.com/nb

Retrieved: 2026-11-16T08:33:27.039641Z; SHA-256 `60131a9f6b70eb88e1abe2f9b17baae58d47a420791b61fcc5b5c155b6d1f860`; locator `company-link:https://www.linkedin.com/company/ginntech`; method `signalpost.website.v1`.

<pre>&lt;a href='https://www.linkedin.com/company/ginntech' class='icon icon-linkedin' target="_blank" aria-label="linkedin"&gt;</pre>

Source: https://ginntech.com/nb

Retrieved: 2026-11-16T08:33:27.039641Z; SHA-256 `60131a9f6b70eb88e1abe2f9b17baae58d47a420791b61fcc5b5c155b6d1f860`; locator `identity-proof:931340476`; method `signalpost.website.v1`.

<pre>ong field--label-hidden field__item"&gt;&lt;p&gt;931340476 MVA&lt;/p&gt;
&lt;/div&gt;
            
  &lt;/div&gt;

    &lt;/div&gt;
  &lt;/div&gt;

  &lt;/div&gt;

            &lt;/div&gt;
            </pre>

### 932296047 - KURVE REGNSKAP AS - social

- url: `https://instagram.com/kurveregnskap`
- proof tier: `own_header_footer_exact_name_v1`
- automated verdict: **correct**

Source: https://kurveregnskap.no/

Retrieved: 2026-11-16T08:30:08.489270Z; SHA-256 `de08b920895bcc6491ad922ef4accc8b6f05d0d63bf14cfafdc468f488c0ba63`; locator `company-link:https://instagram.com/kurveregnskap`; method `signalpost.website.v1`.

<pre>&lt;a target="_blank" rel="noopener" href="https://instagram.com/kurveregnskap"&gt;</pre>

Source: https://kurveregnskap.no/

Retrieved: 2026-11-16T08:30:08.489270Z; SHA-256 `de08b920895bcc6491ad922ef4accc8b6f05d0d63bf14cfafdc468f488c0ba63`; locator `identity-proof:932296047`; method `signalpost.website.v1`.

<pre>egnskap.no&lt;/a&gt;&lt;br&gt;
            Org.nr.: 932296047&lt;br&gt;
            &lt;img decoding="async" src="https://kurveregnskap.no/wp-content/uploads/2025/06/diama</pre>

### 932296047 - KURVE REGNSKAP AS - social

- url: `https://www.facebook.com/kurveregnskap`
- proof tier: `own_header_footer_exact_name_v1`
- automated verdict: **correct**

Source: https://kurveregnskap.no/

Retrieved: 2026-11-16T08:30:08.489270Z; SHA-256 `de08b920895bcc6491ad922ef4accc8b6f05d0d63bf14cfafdc468f488c0ba63`; locator `company-link:https://www.facebook.com/kurveregnskap`; method `signalpost.website.v1`.

<pre>&lt;a target="_blank" rel="noopener" href="https://www.facebook.com/kurveregnskap/"&gt;</pre>

Source: https://kurveregnskap.no/

Retrieved: 2026-11-16T08:30:08.489270Z; SHA-256 `de08b920895bcc6491ad922ef4accc8b6f05d0d63bf14cfafdc468f488c0ba63`; locator `identity-proof:932296047`; method `signalpost.website.v1`.

<pre>egnskap.no&lt;/a&gt;&lt;br&gt;
            Org.nr.: 932296047&lt;br&gt;
            &lt;img decoding="async" src="https://kurveregnskap.no/wp-content/uploads/2025/06/diama</pre>

### 933831922 - SHIFT SECURITY AS - social

- url: `https://www.linkedin.com/company/shift-security-as`
- proof tier: `own_header_footer_exact_name_v1`
- automated verdict: **correct**

Source: https://shiftsecurity.no/

Retrieved: 2026-11-16T08:31:25.833627Z; SHA-256 `c4dd03f1c5a8f0edc4b41d4342c5284d0beb67d1287770be3313fb8c01ad41bb`; locator `company-link:https://www.linkedin.com/company/shift-security-as`; method `signalpost.website.v1`.

<pre>&lt;a href="https://www.linkedin.com/company/shift-security-as/" rel="noopener"&gt;</pre>

Source: https://shiftsecurity.no/personvernerklaring

Retrieved: 2026-11-16T08:31:28.536856Z; SHA-256 `fe56c5e23d3778e10d3c0b193e242a2799f3a57b8262808e022be4fb2822ab72`; locator `identity-proof:933831922`; method `signalpost.website.v1`.

<pre>ift Security AS&lt;br&gt;Organisasjonsnummer: 933 831 922&lt;br&gt;E-post: &lt;a href="mailto:post@shiftsecurity.no" rel="noopener"&gt;post@shiftsecurity.no&lt;/a&gt;&lt;/span&gt;&lt;</pre>

### 987470305 - FLORØ BYGG AS - social

- url: `https://www.facebook.com/florobygg`
- proof tier: `own_header_footer_exact_name_v1`
- automated verdict: **correct**

Source: https://florobygg.no/

Retrieved: 2026-11-16T08:34:32.229499Z; SHA-256 `ddfc23a5574cc31fbc3b09102496494c79e348031012ff6ab6cb313ef0351d95`; locator `company-link:https://www.facebook.com/florobygg`; method `signalpost.website.v1`.

<pre>&lt;a  target="_blank" aria-label="Link to Facebook" href='https://www.facebook.com/florobygg/' data-av_icon='' data-av_iconfont='entypo-fontello' title="Link to Facebook" desc="Link to Facebook" title='Link to Facebook'&gt;</pre>

Source: https://florobygg.no/

Retrieved: 2026-11-16T08:34:32.229499Z; SHA-256 `ddfc23a5574cc31fbc3b09102496494c79e348031012ff6ab6cb313ef0351d95`; locator `identity-proof:987470305`; method `signalpost.website.v1`.

<pre>/sok/detalj.jsp?orgnr=987470305"&gt;Orgnr: 987 470 305&lt;/a&gt;&lt;/p&gt;
&lt;p&gt;Evjegata 10, 6900 FLORØ&lt;/p&gt;
&lt;p&gt;T: &lt;a href="tel:5774770"&gt;57 74 77 00&lt;/a&gt;&lt;/p&gt;
&lt;/div&gt;&lt;/div</pre>

Source: https://florobygg.no/

Retrieved: 2026-11-16T08:34:32.229499Z; SHA-256 `ddfc23a5574cc31fbc3b09102496494c79e348031012ff6ab6cb313ef0351d95`; locator `registry-contact:phone`; method `signalpost.registry_contact.v1`.

<pre>&lt;a href="tel:57747700"&gt;</pre>

### 987470305 - FLORØ BYGG AS - social

- url: `https://www.instagram.com/florobygg`
- proof tier: `own_header_footer_exact_name_v1`
- automated verdict: **correct**

Source: https://florobygg.no/

Retrieved: 2026-11-16T08:34:32.229499Z; SHA-256 `ddfc23a5574cc31fbc3b09102496494c79e348031012ff6ab6cb313ef0351d95`; locator `company-link:https://www.instagram.com/florobygg`; method `signalpost.website.v1`.

<pre>&lt;a  target="_blank" aria-label="Link to Instagram" href='https://www.instagram.com/florobygg/' data-av_icon='' data-av_iconfont='entypo-fontello' title="Link to Instagram" desc="Link to Instagram" title='Link to Instagram'&gt;</pre>

Source: https://florobygg.no/

Retrieved: 2026-11-16T08:34:32.229499Z; SHA-256 `ddfc23a5574cc31fbc3b09102496494c79e348031012ff6ab6cb313ef0351d95`; locator `identity-proof:987470305`; method `signalpost.website.v1`.

<pre>/sok/detalj.jsp?orgnr=987470305"&gt;Orgnr: 987 470 305&lt;/a&gt;&lt;/p&gt;
&lt;p&gt;Evjegata 10, 6900 FLORØ&lt;/p&gt;
&lt;p&gt;T: &lt;a href="tel:5774770"&gt;57 74 77 00&lt;/a&gt;&lt;/p&gt;
&lt;/div&gt;&lt;/div</pre>

Source: https://florobygg.no/

Retrieved: 2026-11-16T08:34:32.229499Z; SHA-256 `ddfc23a5574cc31fbc3b09102496494c79e348031012ff6ab6cb313ef0351d95`; locator `registry-contact:phone`; method `signalpost.registry_contact.v1`.

<pre>&lt;a href="tel:57747700"&gt;</pre>
