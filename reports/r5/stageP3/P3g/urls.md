# P3g scale-500 published website/social inventory

Seed 20261120, 500 companies disjoint from every committed sample, run `r5-p3g-seed20261120-final` from a clean clone. Every published website and social URL is listed with exact saved excerpts, proof tier, retrieval time and SHA-256; each receipt was re-hashed from the saved body and its excerpt found verbatim. Automated verdicts use the existing offline precision-ledger rules (scripts/precision_ledger.py `recheck`); they are rule checks, not human verdicts.

| Kind | Correct | Doubtful | Wrong |
|---|---:|---:|---:|
| website | 36 | 11 | 0 |
| social | 20 | 6 | 14 |

Automated labels are shown exactly as produced. 14 "wrong" label(s) are ledger-tool limitations, not identity findings: `StopIteration` means the legacy recheck found no HTML identity receipt because the site was proven from a linked legal PDF (Stage L2), and "no longer verifies" on `owner_jsonld_sameas_v1` / `own_contact_follow_us_v1` means the legacy social recheck predates the X2 owner-declaration tiers. The full independent verifier (`check_live_run.py`, including `verify_legal_pdf` and `verify_owner_social`) passed every one of them. They stay listed for hand-check below.

## Automated-doubtful or wrong — for hand-check (31)

### 912503259 - OFFICEAID AS - social

- url: `https://www.facebook.com/officeaid.no`
- proof tier: `own_contact_follow_us_v1`
- automated verdict: **wrong** (own header/footer/name/numeric-link policy no longer verifies)

Source: https://www.officeaid.no/kontakt-oss

Retrieved: 2026-11-17T17:35:41.783569Z; SHA-256 `7ce6fd4317fce8eb1ad50be9f1257ce06c4e837cf243fe28eda6a4f66baf1f80`; locator `company-link:https://www.facebook.com/officeaid.no`; method `signalpost.website.v1`.

<pre>&lt;a target="_blank" class="facebook" href="https://www.facebook.com/officeaid.no"&gt;</pre>

Source: https://www.officeaid.no/personvern

Retrieved: 2026-11-17T17:35:40.114245Z; SHA-256 `af0ec3bec00d458e4bc6faec795792ba027a3ed7970f964149a81bcb671a43fd`; locator `identity-proof:912503259`; method `signalpost.website.v1`.

<pre>trong&gt;OfficeAid AS, organisasjonsnummer 912503259 er ansvarlig for behandlingen av personopplysninger og kan ved spørsmål kontaktes på post@officeaid.</pre>

### 912503259 - OFFICEAID AS - social

- url: `https://www.instagram.com/officeaid.no`
- proof tier: `own_contact_follow_us_v1`
- automated verdict: **wrong** (own header/footer/name/numeric-link policy no longer verifies)

Source: https://www.officeaid.no/kontakt-oss

Retrieved: 2026-11-17T17:35:41.783569Z; SHA-256 `7ce6fd4317fce8eb1ad50be9f1257ce06c4e837cf243fe28eda6a4f66baf1f80`; locator `company-link:https://www.instagram.com/officeaid.no`; method `signalpost.website.v1`.

<pre>&lt;a target="_blank" class="instagram" href="https://www.instagram.com/officeaid.no/"&gt;</pre>

Source: https://www.officeaid.no/personvern

Retrieved: 2026-11-17T17:35:40.114245Z; SHA-256 `af0ec3bec00d458e4bc6faec795792ba027a3ed7970f964149a81bcb671a43fd`; locator `identity-proof:912503259`; method `signalpost.website.v1`.

<pre>trong&gt;OfficeAid AS, organisasjonsnummer 912503259 er ansvarlig for behandlingen av personopplysninger og kan ved spørsmål kontaktes på post@officeaid.</pre>

### 916364806 - TT EXPRESS AS - social

- url: `https://www.facebook.com/ttexpressas`
- proof tier: `owner_jsonld_sameas_v1`
- automated verdict: **wrong** (own header/footer/name/numeric-link policy no longer verifies)

Source: https://www.ttexpress.no/

Retrieved: 2026-11-17T17:34:46.072576Z; SHA-256 `9e61edce2a822ed1a26c3244913a2719b70e5ccca16b28c03b74cdd9e901365d`; locator `company-link:https://www.facebook.com/ttexpressas`; method `signalpost.website.v1`.

<pre>\/\/www.ttexpress.no\/#\/schema\/logo\/image\/"},"sameAs":["https:\/\/www.facebook.com\/ttexpressas\/"]}]}</pre>

Source: https://www.ttexpress.no/

Retrieved: 2026-11-17T17:34:46.072576Z; SHA-256 `9e61edce2a822ed1a26c3244913a2719b70e5ccca16b28c03b74cdd9e901365d`; locator `identity-proof:916364806`; method `signalpost.website.v1`.

<pre>     &lt;small&gt;Organisasjonsnummer&lt;/small&gt;
916364806
                        
                    &lt;/div&gt;

                &lt;/div&gt;
            &lt;/div&gt;
     </pre>

### 927525399 - WOODWORKS! CLUSTER - social

- url: `https://www.facebook.com/arenaskog`
- proof tier: `owner_jsonld_sameas_v1`
- automated verdict: **wrong** (own header/footer/name/numeric-link policy no longer verifies)

Source: https://woodworkscluster.no/

Retrieved: 2026-11-17T17:31:45.682612Z; SHA-256 `8e2c2eed3e3549b40dde5c22acd82eaedef946c7e8310918f415d092e369af44`; locator `company-link:https://www.facebook.com/arenaskog`; method `signalpost.website.v1`.

<pre>/woodworkscluster.no\/#\/schema\/logo\/image\/"},"sameAs":["https:\/\/www.facebook.com\/arenaskog\/?fref=ts","https:\/\/linkedin.com\/company\/woodworks-cluster"]}]}</pre>

Source: https://woodworkscluster.no/

Retrieved: 2026-11-17T17:31:45.682612Z; SHA-256 `8e2c2eed3e3549b40dde5c22acd82eaedef946c7e8310918f415d092e369af44`; locator `identity-proof:927525399`; method `signalpost.website.v1`.

<pre>egata 22, 7713 Steinkjer&lt;/p&gt;
&lt;p&gt;Org.nr: 927 525 399&lt;/p&gt;
&lt;p&gt;&lt;a title="Klikk for å lese personvernerklæringen til denne nettsiden" href="https://woodwor</pre>

Source: https://woodworkscluster.no/

Retrieved: 2026-11-17T17:31:45.682612Z; SHA-256 `8e2c2eed3e3549b40dde5c22acd82eaedef946c7e8310918f415d092e369af44`; locator `registry-contact:phone`; method `signalpost.registry_contact.v1`.

<pre>&lt;a title="Ring oss på telefon +47 95 23 90 06" href="tel:+47 95 23 90 06"&gt;</pre>

Source: https://woodworkscluster.no/

Retrieved: 2026-11-17T17:31:45.682612Z; SHA-256 `8e2c2eed3e3549b40dde5c22acd82eaedef946c7e8310918f415d092e369af44`; locator `registry-contact:email_domain`; method `signalpost.registry_contact.v1`.

<pre>&lt;a title="Send e-post til post@woodworkscluster.no" href="mailto:post@woodworkscluster.no"&gt;</pre>

### 966261218 - BØMLO FOLKEHØGSKULE STI - social

- url: `https://www.facebook.com/bomlofhs`
- proof tier: `own_contact_follow_us_v1`
- automated verdict: **wrong** (own header/footer/name/numeric-link policy no longer verifies)

Source: https://bomlo.fhs.no/kontakt/

Retrieved: 2026-11-17T17:36:19.990163Z; SHA-256 `96426be74e058c18dcf8de5254f553e3e7a379b26e6d0590238dc9ce77f16ad0`; locator `company-link:https://www.facebook.com/bomlofhs`; method `signalpost.website.v1`.

<pre>&lt;a href='https://www.facebook.com/bomlofhs' target='_blank' rel='noopener noreferrer'&gt;</pre>

Source: https://bomlo.fhs.no/

Retrieved: 2026-11-17T17:36:15.671188Z; SHA-256 `1ce7249d4ac7be72821e4f9a9232fd7fcc9c469132f3fd3ac82497dfb2dad501`; locator `identity-proof:966261218`; method `signalpost.website.v1`.

<pre>&gt;&lt;!-- wp:paragraph --&gt;
&lt;p&gt;Velkommen til Bømlo folkehøgskule, helt vest i havgapet. Det perfekte stedet for nære øyeblikk og fantastiske eventyr – her hjemme, og der ute i den store verden.&lt;/p&gt;
&lt;!-- /wp:paragraph --&gt;&lt;/div&gt;				&lt;/div&gt;
					&lt;/section&gt;
	&lt;section id="bfhs-linje-grid-container"&gt;
				&lt;div c</pre>

Source: https://bomlo.fhs.no/

Retrieved: 2026-11-17T17:36:15.671188Z; SHA-256 `1ce7249d4ac7be72821e4f9a9232fd7fcc9c469132f3fd3ac82497dfb2dad501`; locator `registry-contact:phone`; method `signalpost.registry_contact.v1`.

<pre>&lt;a class="footer-phone-nr" href="tel:53425650"&gt;</pre>

Source: https://bomlo.fhs.no/

Retrieved: 2026-11-17T17:36:15.671188Z; SHA-256 `1ce7249d4ac7be72821e4f9a9232fd7fcc9c469132f3fd3ac82497dfb2dad501`; locator `registry-contact:email_domain`; method `signalpost.registry_contact.v1`.

<pre>&lt;a href="mailto:post@bomlo.fhs.no"&gt;</pre>

### 966261218 - BØMLO FOLKEHØGSKULE STI - social

- url: `https://www.instagram.com/bomlofhs`
- proof tier: `own_contact_follow_us_v1`
- automated verdict: **wrong** (own header/footer/name/numeric-link policy no longer verifies)

Source: https://bomlo.fhs.no/kontakt/

Retrieved: 2026-11-17T17:36:19.990163Z; SHA-256 `96426be74e058c18dcf8de5254f553e3e7a379b26e6d0590238dc9ce77f16ad0`; locator `company-link:https://www.instagram.com/bomlofhs`; method `signalpost.website.v1`.

<pre>&lt;a href='https://www.instagram.com/bomlofhs/' target='_blank' rel='noopener noreferrer'&gt;</pre>

Source: https://bomlo.fhs.no/

Retrieved: 2026-11-17T17:36:15.671188Z; SHA-256 `1ce7249d4ac7be72821e4f9a9232fd7fcc9c469132f3fd3ac82497dfb2dad501`; locator `identity-proof:966261218`; method `signalpost.website.v1`.

<pre>&gt;&lt;!-- wp:paragraph --&gt;
&lt;p&gt;Velkommen til Bømlo folkehøgskule, helt vest i havgapet. Det perfekte stedet for nære øyeblikk og fantastiske eventyr – her hjemme, og der ute i den store verden.&lt;/p&gt;
&lt;!-- /wp:paragraph --&gt;&lt;/div&gt;				&lt;/div&gt;
					&lt;/section&gt;
	&lt;section id="bfhs-linje-grid-container"&gt;
				&lt;div c</pre>

Source: https://bomlo.fhs.no/

Retrieved: 2026-11-17T17:36:15.671188Z; SHA-256 `1ce7249d4ac7be72821e4f9a9232fd7fcc9c469132f3fd3ac82497dfb2dad501`; locator `registry-contact:phone`; method `signalpost.registry_contact.v1`.

<pre>&lt;a class="footer-phone-nr" href="tel:53425650"&gt;</pre>

Source: https://bomlo.fhs.no/

Retrieved: 2026-11-17T17:36:15.671188Z; SHA-256 `1ce7249d4ac7be72821e4f9a9232fd7fcc9c469132f3fd3ac82497dfb2dad501`; locator `registry-contact:email_domain`; method `signalpost.registry_contact.v1`.

<pre>&lt;a href="mailto:post@bomlo.fhs.no"&gt;</pre>

### 966261218 - BØMLO FOLKEHØGSKULE STI - social

- url: `https://www.tiktok.com/@bomlofhs`
- proof tier: `own_contact_follow_us_v1`
- automated verdict: **wrong** (own header/footer/name/numeric-link policy no longer verifies)

Source: https://bomlo.fhs.no/kontakt/

Retrieved: 2026-11-17T17:36:19.990163Z; SHA-256 `96426be74e058c18dcf8de5254f553e3e7a379b26e6d0590238dc9ce77f16ad0`; locator `company-link:https://www.tiktok.com/@bomlofhs`; method `signalpost.website.v1`.

<pre>&lt;a href='https://www.tiktok.com/@bomlofhs' target='_blank' rel='noopener noreferrer'&gt;</pre>

Source: https://bomlo.fhs.no/

Retrieved: 2026-11-17T17:36:15.671188Z; SHA-256 `1ce7249d4ac7be72821e4f9a9232fd7fcc9c469132f3fd3ac82497dfb2dad501`; locator `identity-proof:966261218`; method `signalpost.website.v1`.

<pre>&gt;&lt;!-- wp:paragraph --&gt;
&lt;p&gt;Velkommen til Bømlo folkehøgskule, helt vest i havgapet. Det perfekte stedet for nære øyeblikk og fantastiske eventyr – her hjemme, og der ute i den store verden.&lt;/p&gt;
&lt;!-- /wp:paragraph --&gt;&lt;/div&gt;				&lt;/div&gt;
					&lt;/section&gt;
	&lt;section id="bfhs-linje-grid-container"&gt;
				&lt;div c</pre>

Source: https://bomlo.fhs.no/

Retrieved: 2026-11-17T17:36:15.671188Z; SHA-256 `1ce7249d4ac7be72821e4f9a9232fd7fcc9c469132f3fd3ac82497dfb2dad501`; locator `registry-contact:phone`; method `signalpost.registry_contact.v1`.

<pre>&lt;a class="footer-phone-nr" href="tel:53425650"&gt;</pre>

Source: https://bomlo.fhs.no/

Retrieved: 2026-11-17T17:36:15.671188Z; SHA-256 `1ce7249d4ac7be72821e4f9a9232fd7fcc9c469132f3fd3ac82497dfb2dad501`; locator `registry-contact:email_domain`; method `signalpost.registry_contact.v1`.

<pre>&lt;a href="mailto:post@bomlo.fhs.no"&gt;</pre>

### 966261218 - BØMLO FOLKEHØGSKULE STI - social

- url: `https://www.youtube.com/channel/UCKY6h9lnepk7TGa-pvYSDdw`
- proof tier: `own_contact_follow_us_v1`
- automated verdict: **wrong** (own header/footer/name/numeric-link policy no longer verifies)

Source: https://bomlo.fhs.no/kontakt/

Retrieved: 2026-11-17T17:36:19.990163Z; SHA-256 `96426be74e058c18dcf8de5254f553e3e7a379b26e6d0590238dc9ce77f16ad0`; locator `company-link:https://www.youtube.com/channel/UCKY6h9lnepk7TGa-pvYSDdw`; method `signalpost.website.v1`.

<pre>&lt;a href='https://www.youtube.com/channel/UCKY6h9lnepk7TGa-pvYSDdw' target='_blank' rel='noopener noreferrer'&gt;</pre>

Source: https://bomlo.fhs.no/

Retrieved: 2026-11-17T17:36:15.671188Z; SHA-256 `1ce7249d4ac7be72821e4f9a9232fd7fcc9c469132f3fd3ac82497dfb2dad501`; locator `identity-proof:966261218`; method `signalpost.website.v1`.

<pre>&gt;&lt;!-- wp:paragraph --&gt;
&lt;p&gt;Velkommen til Bømlo folkehøgskule, helt vest i havgapet. Det perfekte stedet for nære øyeblikk og fantastiske eventyr – her hjemme, og der ute i den store verden.&lt;/p&gt;
&lt;!-- /wp:paragraph --&gt;&lt;/div&gt;				&lt;/div&gt;
					&lt;/section&gt;
	&lt;section id="bfhs-linje-grid-container"&gt;
				&lt;div c</pre>

Source: https://bomlo.fhs.no/

Retrieved: 2026-11-17T17:36:15.671188Z; SHA-256 `1ce7249d4ac7be72821e4f9a9232fd7fcc9c469132f3fd3ac82497dfb2dad501`; locator `registry-contact:phone`; method `signalpost.registry_contact.v1`.

<pre>&lt;a class="footer-phone-nr" href="tel:53425650"&gt;</pre>

Source: https://bomlo.fhs.no/

Retrieved: 2026-11-17T17:36:15.671188Z; SHA-256 `1ce7249d4ac7be72821e4f9a9232fd7fcc9c469132f3fd3ac82497dfb2dad501`; locator `registry-contact:email_domain`; method `signalpost.registry_contact.v1`.

<pre>&lt;a href="mailto:post@bomlo.fhs.no"&gt;</pre>

### 970991786 - VITEC AGRANDO AS - social

- url: `https://www.facebook.com/vitec.agrando`
- proof tier: `own_header_footer_exact_name_v1`
- automated verdict: **doubtful** (No exact target orgnr in saved owner/proof context; published signal-only tier requires hand review; Published identity tier is below exact-number VERIFIED; Saved page proof needs review: corroboration)

Source: https://agrando.no/

Retrieved: 2026-11-17T17:35:38.316805Z; SHA-256 `7efee3d7418e6c3c13a45d6029e6492df42e5fec1430077c2ad35772e162c644`; locator `company-link:https://www.facebook.com/vitec.agrando`; method `signalpost.website.v1`.

<pre>&lt;a href="https://www.facebook.com/vitec.agrando/"&gt;</pre>

Source: https://agrando.no/

Retrieved: 2026-11-17T17:35:38.316805Z; SHA-256 `7efee3d7418e6c3c13a45d6029e6492df42e5fec1430077c2ad35772e162c644`; locator `identity-proof:970991786`; method `signalpost.website.v1`.

<pre>eckCookie();
    });
&lt;/script&gt;&lt;title&gt;
	Vitec Agrando
&lt;/title&gt;&lt;meta id="MetaRobots" name="robots" content="INDEX, FOLLOW" /&gt;&lt;link href="/Portals/_default/skins/polo//skin.css?cdv=932" rel="stylesheet" /&gt;&lt;link href="/Portals/_default/skins/polo//custom.css?cdv=932" rel="stylesheet" /&gt;&lt;link href="/Po</pre>

Source: https://agrando.no/

Retrieved: 2026-11-17T17:35:38.316805Z; SHA-256 `7efee3d7418e6c3c13a45d6029e6492df42e5fec1430077c2ad35772e162c644`; locator `registry-contact:email_domain`; method `signalpost.registry_contact.v1`.

<pre>&lt;a href="mailto:laborasupport.no@vitecsoftware.com"&gt;</pre>

### 985256055 - FRAMEWORKS AS - social

- url: `https://www.facebook.com/FrameworksArendal`
- proof tier: `owner_jsonld_sameas_v1`
- automated verdict: **wrong** (own header/footer/name/numeric-link policy no longer verifies)

Source: https://frameworks.no/

Retrieved: 2026-11-17T17:35:33.256098Z; SHA-256 `09a6f3b7ec8bab0877adfa3b7d56e15bd2693b782ec14d9e8ccabeb9d90d4cfe`; locator `company-link:https://www.facebook.com/FrameworksArendal`; method `signalpost.website.v1`.

<pre>ps:\/\/frameworks.no\/#\/schema\/logo\/image\/"},"sameAs":["https:\/\/www.facebook.com\/FrameworksArendal","https:\/\/www.linkedin.com\/company\/frameworks-as","http</pre>

Source: https://frameworks.no/

Retrieved: 2026-11-17T17:35:33.256098Z; SHA-256 `09a6f3b7ec8bab0877adfa3b7d56e15bd2693b782ec14d9e8ccabeb9d90d4cfe`; locator `identity-proof:985256055`; method `signalpost.website.v1`.

<pre>den 2012. Organisasjonsnummeret vårt er 985 256 055. Du når oss på telefon &lt;a href="tel:+4740400088"&gt;40 40 00 88&lt;/a&gt; eller på &lt;a href="mailto:simen.wi</pre>

Source: https://frameworks.no/

Retrieved: 2026-11-17T17:35:33.256098Z; SHA-256 `09a6f3b7ec8bab0877adfa3b7d56e15bd2693b782ec14d9e8ccabeb9d90d4cfe`; locator `registry-contact:email_domain`; method `signalpost.registry_contact.v1`.

<pre>&lt;a href="mailto:sw@frameworks.no" target="_self" class="e-paragraph-link-base e-default-a"&gt;</pre>

### 985256055 - FRAMEWORKS AS - social

- url: `https://www.instagram.com/frameworks.no`
- proof tier: `owner_jsonld_sameas_v1`
- automated verdict: **wrong** (own header/footer/name/numeric-link policy no longer verifies)

Source: https://frameworks.no/

Retrieved: 2026-11-17T17:35:33.256098Z; SHA-256 `09a6f3b7ec8bab0877adfa3b7d56e15bd2693b782ec14d9e8ccabeb9d90d4cfe`; locator `company-link:https://www.instagram.com/frameworks.no`; method `signalpost.website.v1`.

<pre>ndal","https:\/\/www.linkedin.com\/company\/frameworks-as","https:\/\/www.instagram.com\/frameworks.no\/"]}]}</pre>

Source: https://frameworks.no/

Retrieved: 2026-11-17T17:35:33.256098Z; SHA-256 `09a6f3b7ec8bab0877adfa3b7d56e15bd2693b782ec14d9e8ccabeb9d90d4cfe`; locator `identity-proof:985256055`; method `signalpost.website.v1`.

<pre>den 2012. Organisasjonsnummeret vårt er 985 256 055. Du når oss på telefon &lt;a href="tel:+4740400088"&gt;40 40 00 88&lt;/a&gt; eller på &lt;a href="mailto:simen.wi</pre>

Source: https://frameworks.no/

Retrieved: 2026-11-17T17:35:33.256098Z; SHA-256 `09a6f3b7ec8bab0877adfa3b7d56e15bd2693b782ec14d9e8ccabeb9d90d4cfe`; locator `registry-contact:email_domain`; method `signalpost.registry_contact.v1`.

<pre>&lt;a href="mailto:sw@frameworks.no" target="_self" class="e-paragraph-link-base e-default-a"&gt;</pre>

### 985256055 - FRAMEWORKS AS - social

- url: `https://www.linkedin.com/company/frameworks-as`
- proof tier: `owner_jsonld_sameas_v1`
- automated verdict: **wrong** (own header/footer/name/numeric-link policy no longer verifies)

Source: https://frameworks.no/

Retrieved: 2026-11-17T17:35:33.256098Z; SHA-256 `09a6f3b7ec8bab0877adfa3b7d56e15bd2693b782ec14d9e8ccabeb9d90d4cfe`; locator `company-link:https://www.linkedin.com/company/frameworks-as`; method `signalpost.website.v1`.

<pre>,"sameAs":["https:\/\/www.facebook.com\/FrameworksArendal","https:\/\/www.linkedin.com\/company\/frameworks-as","https:\/\/www.instagram.com\/frameworks.no\/"]}]}</pre>

Source: https://frameworks.no/

Retrieved: 2026-11-17T17:35:33.256098Z; SHA-256 `09a6f3b7ec8bab0877adfa3b7d56e15bd2693b782ec14d9e8ccabeb9d90d4cfe`; locator `identity-proof:985256055`; method `signalpost.website.v1`.

<pre>den 2012. Organisasjonsnummeret vårt er 985 256 055. Du når oss på telefon &lt;a href="tel:+4740400088"&gt;40 40 00 88&lt;/a&gt; eller på &lt;a href="mailto:simen.wi</pre>

Source: https://frameworks.no/

Retrieved: 2026-11-17T17:35:33.256098Z; SHA-256 `09a6f3b7ec8bab0877adfa3b7d56e15bd2693b782ec14d9e8ccabeb9d90d4cfe`; locator `registry-contact:email_domain`; method `signalpost.registry_contact.v1`.

<pre>&lt;a href="mailto:sw@frameworks.no" target="_self" class="e-paragraph-link-base e-default-a"&gt;</pre>

### 986902651 - TINNHEIA BIL AS - social

- url: `https://www.facebook.com/tinnheiabil`
- proof tier: `own_header_footer_exact_name_v1`
- automated verdict: **doubtful** (No exact target orgnr in saved owner/proof context; published signal-only tier requires hand review; Published identity tier is below exact-number VERIFIED; Saved page proof needs review: corroboration)

Source: https://tinnheiabil.no/

Retrieved: 2026-11-17T17:33:01.405390Z; SHA-256 `434f6a1a4f56ee47328ac9e3109bdc3e281baf17ff1a1c9f7b1da14e1a353c9c`; locator `company-link:https://www.facebook.com/tinnheiabil`; method `signalpost.website.v1`.

<pre>&lt;a href="https://www.facebook.com/tinnheiabil/?locale=nb_NO"&gt;</pre>

Source: https://tinnheiabil.no/

Retrieved: 2026-11-17T17:33:01.405390Z; SHA-256 `434f6a1a4f56ee47328ac9e3109bdc3e281baf17ff1a1c9f7b1da14e1a353c9c`; locator `identity-proof:986902651`; method `signalpost.website.v1`.

<pre> 
    &lt;title&gt;Bilverksted Kristiansand - Tinnheia Bil AS&lt;/title&gt;
&lt;meta name="description" content="Bilverksted med EU-kontroll og service på alle bilmerker også elbil og hybrid, AC-service, dekk og dekkhotell, automatgir service. Tinnheia Bil, Kristiansand" /&gt;
&lt;meta property="og:description" content=</pre>

### 990825076 - PECULIUM AS - social

- url: `https://www.instagram.com/peculium_as`
- proof tier: `own_header_footer_exact_name_v1`
- automated verdict: **doubtful** (No exact target orgnr in saved owner/proof context; published signal-only tier requires hand review; Published identity tier is below exact-number VERIFIED; Saved page proof needs review: corroboration)

Source: https://peculium.no/

Retrieved: 2026-11-17T17:34:37.753058Z; SHA-256 `371bf928068d9a8b69328cb82205e5a52bc143313abb7f29b6d1bea2530c1a64`; locator `company-link:https://www.instagram.com/peculium_as`; method `signalpost.website.v1`.

<pre>&lt;a class="text-gray-400 hover:opacity-80 transition-opacity" target="_blank" rel="noreferrer" href="https://www.instagram.com/peculium_as/"&gt;</pre>

Source: https://peculium.no/kontakt

Retrieved: 2026-11-17T17:34:40.683770Z; SHA-256 `f765c4a15fd2a63af7e7b6e6f049cc83dc296668259afe3b45873f86543c4f84`; locator `identity-proof:990825076`; method `signalpost.website.v1`.

<pre>:1","S:1")&lt;/script&gt;&lt;title&gt;Kontakt oss - Peculium AS | Eiendomsforvaltning i Porsgrunn&lt;/title&gt;&lt;meta name="description" content="Ta kontakt med Peculium AS for eiendomsforvaltning og utleie i Porsgrunn. Vi hjelper deg med lokaler, næringsbygg og boligutleie. Ring eller send e-post."/&gt;&lt;meta name="autho</pre>

### 991323848 - TROLLHEIM AS - social

- url: `https://facebook.com/TrollheimAS`
- proof tier: `own_header_footer_exact_name_v1`
- automated verdict: **doubtful** (No exact target orgnr in saved owner/proof context; published signal-only tier requires hand review; Published identity tier is below exact-number VERIFIED; Saved page proof needs review: corroboration)

Source: https://trollheim.no/

Retrieved: 2026-11-17T17:33:18.184369Z; SHA-256 `15f2a742f2d0baf7a6ba588677bd54709bdf264771c719f4519a33d081d92e4a`; locator `company-link:https://facebook.com/TrollheimAS`; method `signalpost.website.v1`.

<pre>&lt;a class="elementor-icon elementor-social-icon elementor-social-icon-facebook-f elementor-repeater-item-4f37a04" href="https://facebook.com/TrollheimAS" target="_blank"&gt;</pre>

Source: https://trollheim.no/

Retrieved: 2026-11-17T17:33:18.184369Z; SHA-256 `15f2a742f2d0baf7a6ba588677bd54709bdf264771c719f4519a33d081d92e4a`; locator `identity-proof:991323848`; method `signalpost.website.v1`.

<pre>9mefvgt6v6z5ncrt7e8vatuv2ns0y" /&gt;&lt;title&gt;Trollheim &amp;#8211; Arbeid og inkludering&lt;/title&gt;
&lt;meta name='robots' content='max-image-preview:large' /&gt;

&lt;script&gt;
dataLayer = [{"title":"Hjem","author":"Webmaster","wordcount":66,"logged_in":"false","page_id":47,"post_date":"2018-01-25 14:20:00"}];
&lt;/script&gt;
</pre>

Source: https://trollheim.no/

Retrieved: 2026-11-17T17:33:18.184369Z; SHA-256 `15f2a742f2d0baf7a6ba588677bd54709bdf264771c719f4519a33d081d92e4a`; locator `registry-contact:email_domain`; method `signalpost.registry_contact.v1`.

<pre>&lt;a href="mailto:post@trollheim.no"&gt;</pre>

Source: https://trollheim.no/

Retrieved: 2026-11-17T17:33:18.184369Z; SHA-256 `15f2a742f2d0baf7a6ba588677bd54709bdf264771c719f4519a33d081d92e4a`; locator `registry-contact:phone`; method `signalpost.registry_contact.v1`.

<pre>="color: #000000;"&gt;Trollheim &amp;#8211; Tlf. 71 65 77 77 &amp;#8211; &lt;strong&gt;&lt;a href="mailto:post@trollheim.no"&gt;post@trollheim.no&lt;/a&gt;&lt;/strong&gt;&lt;/span&gt;&lt;br /&gt;&lt;span style="color: #000000;"&gt;Trollheim avd. Røtet/Hovedkontor: Industrivegen 63, 6652 Surnadal&lt;/span&gt;&lt;br /&gt;&lt;span style="color: #000000;"&gt;Trollheim avd.</pre>

### 991323848 - TROLLHEIM AS - social

- url: `https://twitter.com/TrollheimAS`
- proof tier: `own_header_footer_exact_name_v1`
- automated verdict: **doubtful** (No exact target orgnr in saved owner/proof context; published signal-only tier requires hand review; Published identity tier is below exact-number VERIFIED; Saved page proof needs review: corroboration)

Source: https://trollheim.no/

Retrieved: 2026-11-17T17:33:18.184369Z; SHA-256 `15f2a742f2d0baf7a6ba588677bd54709bdf264771c719f4519a33d081d92e4a`; locator `company-link:https://twitter.com/TrollheimAS`; method `signalpost.website.v1`.

<pre>&lt;a class="elementor-icon elementor-social-icon elementor-social-icon-twitter elementor-repeater-item-e32e197" href="https://twitter.com/TrollheimAS" target="_blank"&gt;</pre>

Source: https://trollheim.no/

Retrieved: 2026-11-17T17:33:18.184369Z; SHA-256 `15f2a742f2d0baf7a6ba588677bd54709bdf264771c719f4519a33d081d92e4a`; locator `identity-proof:991323848`; method `signalpost.website.v1`.

<pre>9mefvgt6v6z5ncrt7e8vatuv2ns0y" /&gt;&lt;title&gt;Trollheim &amp;#8211; Arbeid og inkludering&lt;/title&gt;
&lt;meta name='robots' content='max-image-preview:large' /&gt;

&lt;script&gt;
dataLayer = [{"title":"Hjem","author":"Webmaster","wordcount":66,"logged_in":"false","page_id":47,"post_date":"2018-01-25 14:20:00"}];
&lt;/script&gt;
</pre>

Source: https://trollheim.no/

Retrieved: 2026-11-17T17:33:18.184369Z; SHA-256 `15f2a742f2d0baf7a6ba588677bd54709bdf264771c719f4519a33d081d92e4a`; locator `registry-contact:email_domain`; method `signalpost.registry_contact.v1`.

<pre>&lt;a href="mailto:post@trollheim.no"&gt;</pre>

Source: https://trollheim.no/

Retrieved: 2026-11-17T17:33:18.184369Z; SHA-256 `15f2a742f2d0baf7a6ba588677bd54709bdf264771c719f4519a33d081d92e4a`; locator `registry-contact:phone`; method `signalpost.registry_contact.v1`.

<pre>="color: #000000;"&gt;Trollheim &amp;#8211; Tlf. 71 65 77 77 &amp;#8211; &lt;strong&gt;&lt;a href="mailto:post@trollheim.no"&gt;post@trollheim.no&lt;/a&gt;&lt;/strong&gt;&lt;/span&gt;&lt;br /&gt;&lt;span style="color: #000000;"&gt;Trollheim avd. Røtet/Hovedkontor: Industrivegen 63, 6652 Surnadal&lt;/span&gt;&lt;br /&gt;&lt;span style="color: #000000;"&gt;Trollheim avd.</pre>

### 991323848 - TROLLHEIM AS - social

- url: `https://www.instagram.com/trollheimas`
- proof tier: `own_header_footer_exact_name_v1`
- automated verdict: **doubtful** (No exact target orgnr in saved owner/proof context; published signal-only tier requires hand review; Published identity tier is below exact-number VERIFIED; Saved page proof needs review: corroboration)

Source: https://trollheim.no/

Retrieved: 2026-11-17T17:33:18.184369Z; SHA-256 `15f2a742f2d0baf7a6ba588677bd54709bdf264771c719f4519a33d081d92e4a`; locator `company-link:https://www.instagram.com/trollheimas`; method `signalpost.website.v1`.

<pre>&lt;a class="elementor-icon elementor-social-icon elementor-social-icon-instagram elementor-repeater-item-34dd5a2" href="https://www.instagram.com/trollheimas/" target="_blank"&gt;</pre>

Source: https://trollheim.no/

Retrieved: 2026-11-17T17:33:18.184369Z; SHA-256 `15f2a742f2d0baf7a6ba588677bd54709bdf264771c719f4519a33d081d92e4a`; locator `identity-proof:991323848`; method `signalpost.website.v1`.

<pre>9mefvgt6v6z5ncrt7e8vatuv2ns0y" /&gt;&lt;title&gt;Trollheim &amp;#8211; Arbeid og inkludering&lt;/title&gt;
&lt;meta name='robots' content='max-image-preview:large' /&gt;

&lt;script&gt;
dataLayer = [{"title":"Hjem","author":"Webmaster","wordcount":66,"logged_in":"false","page_id":47,"post_date":"2018-01-25 14:20:00"}];
&lt;/script&gt;
</pre>

Source: https://trollheim.no/

Retrieved: 2026-11-17T17:33:18.184369Z; SHA-256 `15f2a742f2d0baf7a6ba588677bd54709bdf264771c719f4519a33d081d92e4a`; locator `registry-contact:email_domain`; method `signalpost.registry_contact.v1`.

<pre>&lt;a href="mailto:post@trollheim.no"&gt;</pre>

Source: https://trollheim.no/

Retrieved: 2026-11-17T17:33:18.184369Z; SHA-256 `15f2a742f2d0baf7a6ba588677bd54709bdf264771c719f4519a33d081d92e4a`; locator `registry-contact:phone`; method `signalpost.registry_contact.v1`.

<pre>="color: #000000;"&gt;Trollheim &amp;#8211; Tlf. 71 65 77 77 &amp;#8211; &lt;strong&gt;&lt;a href="mailto:post@trollheim.no"&gt;post@trollheim.no&lt;/a&gt;&lt;/strong&gt;&lt;/span&gt;&lt;br /&gt;&lt;span style="color: #000000;"&gt;Trollheim avd. Røtet/Hovedkontor: Industrivegen 63, 6652 Surnadal&lt;/span&gt;&lt;br /&gt;&lt;span style="color: #000000;"&gt;Trollheim avd.</pre>

### 994479865 - IDENTUM AS - social

- url: `https://twitter.com/IAM_Identum`
- proof tier: `own_contact_follow_us_v1`
- automated verdict: **wrong** (own header/footer/name/numeric-link policy no longer verifies)

Source: https://www.identum.no/kontakt

Retrieved: 2026-11-17T17:32:02.930741Z; SHA-256 `0a7b75899edc756ec1ed67721be022fda9265762314a53377ed1519905a19a65`; locator `company-link:https://twitter.com/IAM_Identum`; method `signalpost.website.v1`.

<pre>&lt;a class="default-link nav-list__link " href="https://twitter.com/IAM_Identum" target="_blank"&gt;</pre>

Source: https://www.identum.no/

Retrieved: 2026-11-17T17:32:01.564168Z; SHA-256 `356223741f48deba792eff2c569e1b2a0b4bdee0c59d567e77912eb72e1301d0`; locator `identity-proof:994479865`; method `signalpost.website.v1`.

<pre>"&gt;Organisasjonsnummer&lt;/h3&gt;
        &lt;p&gt;NO994479865 MVA&lt;/p&gt;
      &lt;/li&gt;
    
    &lt;/ul&gt;
  
&lt;/div&gt;
&lt;/div&gt;
        
      &lt;/div&gt;
      &lt;div class="footer-i</pre>

### 994479865 - IDENTUM AS - social

- url: `https://www.facebook.com/identum.no`
- proof tier: `own_contact_follow_us_v1`
- automated verdict: **wrong** (own header/footer/name/numeric-link policy no longer verifies)

Source: https://www.identum.no/kontakt

Retrieved: 2026-11-17T17:32:02.930741Z; SHA-256 `0a7b75899edc756ec1ed67721be022fda9265762314a53377ed1519905a19a65`; locator `company-link:https://www.facebook.com/identum.no`; method `signalpost.website.v1`.

<pre>&lt;a class="default-link nav-list__link " href="https://www.facebook.com/identum.no" target="_blank"&gt;</pre>

Source: https://www.identum.no/

Retrieved: 2026-11-17T17:32:01.564168Z; SHA-256 `356223741f48deba792eff2c569e1b2a0b4bdee0c59d567e77912eb72e1301d0`; locator `identity-proof:994479865`; method `signalpost.website.v1`.

<pre>"&gt;Organisasjonsnummer&lt;/h3&gt;
        &lt;p&gt;NO994479865 MVA&lt;/p&gt;
      &lt;/li&gt;
    
    &lt;/ul&gt;
  
&lt;/div&gt;
&lt;/div&gt;
        
      &lt;/div&gt;
      &lt;div class="footer-i</pre>

### 994479865 - IDENTUM AS - social

- url: `https://www.instagram.com/iam_identum`
- proof tier: `own_contact_follow_us_v1`
- automated verdict: **wrong** (own header/footer/name/numeric-link policy no longer verifies)

Source: https://www.identum.no/kontakt

Retrieved: 2026-11-17T17:32:02.930741Z; SHA-256 `0a7b75899edc756ec1ed67721be022fda9265762314a53377ed1519905a19a65`; locator `company-link:https://www.instagram.com/iam_identum`; method `signalpost.website.v1`.

<pre>&lt;a class="default-link nav-list__link " href="https://www.instagram.com/iam_identum/" target="_blank"&gt;</pre>

Source: https://www.identum.no/

Retrieved: 2026-11-17T17:32:01.564168Z; SHA-256 `356223741f48deba792eff2c569e1b2a0b4bdee0c59d567e77912eb72e1301d0`; locator `identity-proof:994479865`; method `signalpost.website.v1`.

<pre>"&gt;Organisasjonsnummer&lt;/h3&gt;
        &lt;p&gt;NO994479865 MVA&lt;/p&gt;
      &lt;/li&gt;
    
    &lt;/ul&gt;
  
&lt;/div&gt;
&lt;/div&gt;
        
      &lt;/div&gt;
      &lt;div class="footer-i</pre>

### 833242482 - SOLI AUTO AS - website

- url: `https://soliauto.no`
- proof tier: `publisher_name_registered_place`
- identity level: `HIGH`
- automated verdict: **doubtful** (No exact target orgnr in saved owner/proof context; published signal-only tier requires hand review; Published identity tier is below exact-number VERIFIED; Saved page proof needs review: corroboration)

Source: https://soliauto.no/

Retrieved: 2026-11-17T17:35:06.492568Z; SHA-256 `f54759e88e0bb834dbc458f137395762dd4322d9c3d3daf43f9a3a773a64a67b`; locator `identity-proof:833242482`; method `signalpost.website.v1`.

<pre>roduct/yoast-seo-wordpress/ --&gt;
	&lt;title&gt;Soli Auto As - Soli Auto As&lt;/title&gt;
	&lt;meta name="description" content="Soli Auto AS tilbyr salg av bruktbil, innbytte og fleksible finansieringsløsninger i Fredrikstad og omegn. Bilforhandler som tar bilkjøp på alvor." /&gt;
	&lt;link rel="canonical" href="https://s</pre>

### 926765655 - LISTER LASERKLINIKK AS - website

- url: `https://listerlaserklinikk.no`
- proof tier: `publisher_name_registered_place`
- identity level: `HIGH`
- automated verdict: **doubtful** (No exact target orgnr in saved owner/proof context; published signal-only tier requires hand review; Published identity tier is below exact-number VERIFIED; Saved page proof needs review: corroboration)

Source: https://listerlaserklinikk.no/

Retrieved: 2026-11-17T17:35:26.420068Z; SHA-256 `a4ac4880b4b705181acc7d08c503561135f1764efa3a01836a48b9e20c6afcec`; locator `identity-proof:926765655`; method `signalpost.website.v1`.

<pre>ant"&gt;&lt;head&gt;&lt;meta charset="utf-8"&gt;&lt;title&gt;Lister laserklinikk AS&lt;/title&gt;&lt;meta name="robots" content="all"&gt;&lt;meta name="generator" content="One.com Web Editor"&gt;&lt;meta http-equiv="Cache-Control" content="must-revalidate, max-age=0, public"&gt;&lt;meta http-equiv="Expires" content="-1"&gt;&lt;meta name="viewport" cont</pre>

### 930595764 - WESTNES HOLDING AS - website

- url: `https://westnesholding.no`
- proof tier: `orgnr_on_page`
- identity level: `VERIFIED`
- automated verdict: **doubtful** (Group/multi-company site context needs hand review)

Source: https://westnesholding.no/

Retrieved: 2026-11-17T17:32:49.817413Z; SHA-256 `89403e39c0c2d07730063ba4c81516bbb9474c864cf4cbaafe1a5c4f81f39c07`; locator `identity-proof:930595764`; method `signalpost.website.v1`.

<pre>nes Holding AS&lt;/div&gt;
      &lt;div&gt;Org.nr. 930 595 764&lt;/div&gt;
    &lt;/div&gt;
  &lt;/footer&gt;
&lt;/div&gt;

&lt;/body&gt;
&lt;/html&gt;
</pre>

### 954583996 - HVALSAFARI AS - website

- url: `https://whalesafari.no`
- proof tier: `registry_declared_publisher_name`
- identity level: `HIGH`
- automated verdict: **doubtful** (No exact target orgnr in saved owner/proof context; published signal-only tier requires hand review; Published identity tier is below exact-number VERIFIED; Saved page proof needs review: corroboration)

Source: https://whalesafari.no/

Retrieved: 2026-11-17T17:34:25.680939Z; SHA-256 `0ab1bb56e830d625cf901c11cb68cdd6de6f046cd5c92c3bc2a1352f0a0a748f`; locator `identity-proof:954583996`; method `signalpost.website.v1`.

<pre>12"&gt;
                    Whale2Sea AS / Hvalsafari AS &lt;br /&gt;
Hamnegata 1C&lt;br /&gt;
8480 Andenes, Norway&lt;br /&gt;
Email: whale2sea@whalesafari.no&lt;br /&gt;
Phone: +47 76 11 56 00 / 91 67 49 60
                &lt;/div&gt;
            
        &lt;/div&gt;

        &lt;div class="flex flex-col lg:grow lg:px-1/12  lg:flex-row </pre>

Source: https://whalesafari.no/

Retrieved: 2026-11-17T17:34:25.680939Z; SHA-256 `0ab1bb56e830d625cf901c11cb68cdd6de6f046cd5c92c3bc2a1352f0a0a748f`; locator `registry-contact:phone`; method `signalpost.registry_contact.v1`.

<pre>: whale2sea@whalesafari.no&lt;br /&gt;
Phone: +47 76 11 56 00 / 91 67 49 60
                &lt;/div&gt;
            
        &lt;/div&gt;

        &lt;div class="flex flex-col lg:grow lg:px-1/12  lg:flex-row lg:justify-around "&gt;
            &lt;div class="lg:mr-1/6"&gt;
                &lt;ul class="space-y-5 lg:space-y-6 text-</pre>

Source: https://whalesafari.no/

Retrieved: 2026-11-17T17:34:25.680939Z; SHA-256 `0ab1bb56e830d625cf901c11cb68cdd6de6f046cd5c92c3bc2a1352f0a0a748f`; locator `registry-contact:email_domain`; method `signalpost.registry_contact.v1`.

<pre>br /&gt;
8480 Andenes, Norway&lt;br /&gt;
Email: whale2sea@whalesafari.no&lt;br /&gt;
Phone: +47 76 11 56 00 / 91 67 49 60
                &lt;/div&gt;
            
        &lt;/div&gt;

        &lt;div class="flex flex-col lg:grow lg:px-1/12  lg:flex-row lg:justify-around "&gt;
            &lt;div class="lg:mr-1/6"&gt;
                &lt;</pre>

### 966261218 - BØMLO FOLKEHØGSKULE STI - website

- url: `https://bomlo.fhs.no`
- proof tier: `signals`
- identity level: `HIGH`
- automated verdict: **doubtful** (No exact target orgnr in saved owner/proof context; published signal-only tier requires hand review; Published identity tier is below exact-number VERIFIED; Saved page proof needs review: corroboration)

Source: https://bomlo.fhs.no/

Retrieved: 2026-11-17T17:36:15.671188Z; SHA-256 `1ce7249d4ac7be72821e4f9a9232fd7fcc9c469132f3fd3ac82497dfb2dad501`; locator `identity-proof:966261218`; method `signalpost.website.v1`.

<pre>&gt;&lt;!-- wp:paragraph --&gt;
&lt;p&gt;Velkommen til Bømlo folkehøgskule, helt vest i havgapet. Det perfekte stedet for nære øyeblikk og fantastiske eventyr – her hjemme, og der ute i den store verden.&lt;/p&gt;
&lt;!-- /wp:paragraph --&gt;&lt;/div&gt;				&lt;/div&gt;
					&lt;/section&gt;
	&lt;section id="bfhs-linje-grid-container"&gt;
				&lt;div c</pre>

Source: https://bomlo.fhs.no/

Retrieved: 2026-11-17T17:36:15.671188Z; SHA-256 `1ce7249d4ac7be72821e4f9a9232fd7fcc9c469132f3fd3ac82497dfb2dad501`; locator `registry-contact:phone`; method `signalpost.registry_contact.v1`.

<pre>&lt;a class="footer-phone-nr" href="tel:53425650"&gt;</pre>

Source: https://bomlo.fhs.no/

Retrieved: 2026-11-17T17:36:15.671188Z; SHA-256 `1ce7249d4ac7be72821e4f9a9232fd7fcc9c469132f3fd3ac82497dfb2dad501`; locator `registry-contact:email_domain`; method `signalpost.registry_contact.v1`.

<pre>&lt;a href="mailto:post@bomlo.fhs.no"&gt;</pre>

### 970991786 - VITEC AGRANDO AS - website

- url: `https://agrando.no`
- proof tier: `signals`
- identity level: `HIGH`
- automated verdict: **doubtful** (No exact target orgnr in saved owner/proof context; published signal-only tier requires hand review; Published identity tier is below exact-number VERIFIED; Saved page proof needs review: corroboration)

Source: https://agrando.no/

Retrieved: 2026-11-17T17:35:38.316805Z; SHA-256 `7efee3d7418e6c3c13a45d6029e6492df42e5fec1430077c2ad35772e162c644`; locator `identity-proof:970991786`; method `signalpost.website.v1`.

<pre>eckCookie();
    });
&lt;/script&gt;&lt;title&gt;
	Vitec Agrando
&lt;/title&gt;&lt;meta id="MetaRobots" name="robots" content="INDEX, FOLLOW" /&gt;&lt;link href="/Portals/_default/skins/polo//skin.css?cdv=932" rel="stylesheet" /&gt;&lt;link href="/Portals/_default/skins/polo//custom.css?cdv=932" rel="stylesheet" /&gt;&lt;link href="/Po</pre>

Source: https://agrando.no/

Retrieved: 2026-11-17T17:35:38.316805Z; SHA-256 `7efee3d7418e6c3c13a45d6029e6492df42e5fec1430077c2ad35772e162c644`; locator `registry-contact:email_domain`; method `signalpost.registry_contact.v1`.

<pre>&lt;a href="mailto:laborasupport.no@vitecsoftware.com"&gt;</pre>

### 986902651 - TINNHEIA BIL AS - website

- url: `https://tinnheiabil.no`
- proof tier: `publisher_name_registered_place`
- identity level: `HIGH`
- automated verdict: **doubtful** (No exact target orgnr in saved owner/proof context; published signal-only tier requires hand review; Published identity tier is below exact-number VERIFIED; Saved page proof needs review: corroboration)

Source: https://tinnheiabil.no/

Retrieved: 2026-11-17T17:33:01.405390Z; SHA-256 `434f6a1a4f56ee47328ac9e3109bdc3e281baf17ff1a1c9f7b1da14e1a353c9c`; locator `identity-proof:986902651`; method `signalpost.website.v1`.

<pre> 
    &lt;title&gt;Bilverksted Kristiansand - Tinnheia Bil AS&lt;/title&gt;
&lt;meta name="description" content="Bilverksted med EU-kontroll og service på alle bilmerker også elbil og hybrid, AC-service, dekk og dekkhotell, automatgir service. Tinnheia Bil, Kristiansand" /&gt;
&lt;meta property="og:description" content=</pre>

### 988911879 - ELVEGATA 16 AS - website

- url: `https://www.elvegata16.no`
- proof tier: `publisher_name_rare_contact`
- identity level: `HIGH`
- automated verdict: **doubtful** (No exact target orgnr in saved owner/proof context; published signal-only tier requires hand review; Published identity tier is below exact-number VERIFIED; Saved page proof needs review: corroboration)

Source: https://www.elvegata16.no/kontakt/

Retrieved: 2026-11-17T17:33:57.603888Z; SHA-256 `9e49a1cb80171d5eedc70bf9309b98b589147d383f9626e3da54b4b7e71aa961`; locator `identity-proof:988911879`; method `signalpost.website.v1`.

<pre>&lt;span class="b-l-text-c logo-text-cell"&gt;Elvegata 16 AS&lt;/span&gt;
				&lt;/div&gt;
			&lt;/div&gt;

		&lt;/a&gt;
	&lt;/div&gt;
&lt;/div&gt;
						&lt;/div&gt;

						&lt;div id="menu-slider"&gt;
							&lt;div id="menu-block"&gt;
								&lt;nav id="menu"&gt;&lt;div class="menu-font menu-wrapper"&gt;
	&lt;a href="#" class="menu-close" rel="nofollow" title="Cl</pre>

### 990825076 - PECULIUM AS - website

- url: `https://peculium.no`
- proof tier: `publisher_name_registered_place`
- identity level: `HIGH`
- automated verdict: **doubtful** (No exact target orgnr in saved owner/proof context; published signal-only tier requires hand review; Published identity tier is below exact-number VERIFIED; Saved page proof needs review: corroboration)

Source: https://peculium.no/kontakt

Retrieved: 2026-11-17T17:34:40.683770Z; SHA-256 `f765c4a15fd2a63af7e7b6e6f049cc83dc296668259afe3b45873f86543c4f84`; locator `identity-proof:990825076`; method `signalpost.website.v1`.

<pre>:1","S:1")&lt;/script&gt;&lt;title&gt;Kontakt oss - Peculium AS | Eiendomsforvaltning i Porsgrunn&lt;/title&gt;&lt;meta name="description" content="Ta kontakt med Peculium AS for eiendomsforvaltning og utleie i Porsgrunn. Vi hjelper deg med lokaler, næringsbygg og boligutleie. Ring eller send e-post."/&gt;&lt;meta name="autho</pre>

### 991323848 - TROLLHEIM AS - website

- url: `https://trollheim.no`
- proof tier: `signals`
- identity level: `HIGH`
- automated verdict: **doubtful** (No exact target orgnr in saved owner/proof context; published signal-only tier requires hand review; Published identity tier is below exact-number VERIFIED; Saved page proof needs review: corroboration)

Source: https://trollheim.no/

Retrieved: 2026-11-17T17:33:18.184369Z; SHA-256 `15f2a742f2d0baf7a6ba588677bd54709bdf264771c719f4519a33d081d92e4a`; locator `identity-proof:991323848`; method `signalpost.website.v1`.

<pre>9mefvgt6v6z5ncrt7e8vatuv2ns0y" /&gt;&lt;title&gt;Trollheim &amp;#8211; Arbeid og inkludering&lt;/title&gt;
&lt;meta name='robots' content='max-image-preview:large' /&gt;

&lt;script&gt;
dataLayer = [{"title":"Hjem","author":"Webmaster","wordcount":66,"logged_in":"false","page_id":47,"post_date":"2018-01-25 14:20:00"}];
&lt;/script&gt;
</pre>

Source: https://trollheim.no/

Retrieved: 2026-11-17T17:33:18.184369Z; SHA-256 `15f2a742f2d0baf7a6ba588677bd54709bdf264771c719f4519a33d081d92e4a`; locator `registry-contact:email_domain`; method `signalpost.registry_contact.v1`.

<pre>&lt;a href="mailto:post@trollheim.no"&gt;</pre>

Source: https://trollheim.no/

Retrieved: 2026-11-17T17:33:18.184369Z; SHA-256 `15f2a742f2d0baf7a6ba588677bd54709bdf264771c719f4519a33d081d92e4a`; locator `registry-contact:phone`; method `signalpost.registry_contact.v1`.

<pre>="color: #000000;"&gt;Trollheim &amp;#8211; Tlf. 71 65 77 77 &amp;#8211; &lt;strong&gt;&lt;a href="mailto:post@trollheim.no"&gt;post@trollheim.no&lt;/a&gt;&lt;/strong&gt;&lt;/span&gt;&lt;br /&gt;&lt;span style="color: #000000;"&gt;Trollheim avd. Røtet/Hovedkontor: Industrivegen 63, 6652 Surnadal&lt;/span&gt;&lt;br /&gt;&lt;span style="color: #000000;"&gt;Trollheim avd.</pre>

### 998407257 - GRAVITONIA AS - website

- url: `https://www.gravitonia.com`
- proof tier: `registry_declared_live`
- identity level: `HIGH`
- automated verdict: **doubtful** (No exact target orgnr in saved owner/proof context; published signal-only tier requires hand review; Published identity tier is below exact-number VERIFIED; Saved page proof needs review: corroboration)

Source: https://www.gravitonia.com/

Retrieved: 2026-11-17T17:35:06.784014Z; SHA-256 `1cef1b2d430c916ae3e8acaa42188c00fc98019dcdc898e801b1225966e20941`; locator `identity-proof:998407257`; method `signalpost.website.v1`.

<pre>mayozfLeqJg="
  }
}&lt;/script&gt;
    &lt;title&gt;Gravitonia&lt;/title&gt;&lt;/head&gt;

&lt;body&gt;&lt;div class="page" b-vyzgrxpymy&gt;&lt;header&gt;&lt;div class="container nav-flex"&gt;&lt;a href="/" class="brand" data-enhance-nav="false"&gt;&lt;img height="32px" width="32px" src="images/gravitonia-logo-32.jpg" alt="Gravitonia Logo" class="logo"&gt;
 </pre>

## Website — automated correct (36)

### 820365682 - WELL INTERCEPT AS - website

- url: `https://www.wellintercept.no`
- proof tier: `orgnr_on_page`
- identity level: `VERIFIED`
- automated verdict: **correct**

Source: https://www.wellintercept.no/

Retrieved: 2026-11-17T17:32:44.016982Z; SHA-256 `1692bfc22c7ca97af1b79442255f911169bbbf4a0941db87f8c9fa729177a90e`; locator `identity-proof:820365682`; method `signalpost.website.v1`.

<pre>en 22&lt;br&gt;

4050 Sola&lt;br&gt;
&lt;br&gt;

Org nr.: 820 365 682&lt;/h4&gt;		&lt;/div&gt;
				&lt;/div&gt;
				&lt;div class="elementor-element elementor-element-44ad79c elementor-hidd</pre>

### 831854812 - COLIFT AS - website

- url: `https://colift.no`
- proof tier: `orgnr_on_page`
- identity level: `VERIFIED`
- automated verdict: **correct**

Source: https://colift.no/

Retrieved: 2026-11-17T17:34:43.062882Z; SHA-256 `f28e3f67d1ec5fdbf5103e49e7baa2f7e8c126dd066354ec8651aaf113b15d99`; locator `identity-proof:831854812`; method `signalpost.website.v1`.

<pre>s tw:space-y-2 tw:p-0"&gt;&lt;li&gt;© COLIFT AS (831 854 812)&lt;/li&gt;&lt;li class="tw:flex tw:items-center tw:gap-2"&gt;&lt;svg aria-hidden="true" focusable="false" viewBo</pre>

### 855197812 - ADVOKATFIRMAET ECKHOFF FOSMARK & CO DA - website

- url: `https://www.eckfos.no`
- proof tier: `orgnr_on_page`
- identity level: `VERIFIED`
- automated verdict: **correct**

Source: https://www.eckfos.no/

Retrieved: 2026-11-17T17:34:58.898269Z; SHA-256 `e94923689490201511f829838d34aa8412716b714cae2a66f863decdd09eb421`; locator `identity-proof:855197812`; method `signalpost.website.v1`.

<pre>n: 23 08 57 20&lt;br /&gt;
Organisasjonsnr.: 855 197 812&lt;br /&gt;
&lt;br /&gt;
For spørsmål du måtte ha om vår behandling av personopplysninger kan du kontakte os</pre>

Source: https://www.eckfos.no/

Retrieved: 2026-11-17T17:34:58.898269Z; SHA-256 `e94923689490201511f829838d34aa8412716b714cae2a66f863decdd09eb421`; locator `registry-contact:phone`; method `signalpost.registry_contact.v1`.

<pre>
E-post: post@eckfos.no&lt;br /&gt;
Telefon: 23 08 57 20&lt;br /&gt;
Organisasjonsnr.: 855 197 812&lt;br /&gt;
&lt;br /&gt;
For spørsmål du måtte ha om vår behandling av personopplysninger kan du kontakte oss.&lt;br /&gt;
&lt;br /&gt;
Vår nettstedsadresse er: https://www.eckfos.no&lt;br /&gt;
&lt;br /&gt;
Advokatfirmaet Eckhoff, Fosmark &amp;</pre>

Source: https://www.eckfos.no/

Retrieved: 2026-11-17T17:34:58.898269Z; SHA-256 `e94923689490201511f829838d34aa8412716b714cae2a66f863decdd09eb421`; locator `registry-contact:email_domain`; method `signalpost.registry_contact.v1`.

<pre> Solli, 0203 Oslo (post)&lt;br /&gt;
E-post: post@eckfos.no&lt;br /&gt;
Telefon: 23 08 57 20&lt;br /&gt;
Organisasjonsnr.: 855 197 812&lt;br /&gt;
&lt;br /&gt;
For spørsmål du måtte ha om vår behandling av personopplysninger kan du kontakte oss.&lt;br /&gt;
&lt;br /&gt;
Vår nettstedsadresse er: https://www.eckfos.no&lt;br /&gt;
&lt;br /&gt;
Ad</pre>

### 912503259 - OFFICEAID AS - website

- url: `https://www.officeaid.no`
- proof tier: `orgnr_on_page`
- identity level: `VERIFIED`
- automated verdict: **correct**

Source: https://www.officeaid.no/personvern

Retrieved: 2026-11-17T17:35:40.114245Z; SHA-256 `af0ec3bec00d458e4bc6faec795792ba027a3ed7970f964149a81bcb671a43fd`; locator `identity-proof:912503259`; method `signalpost.website.v1`.

<pre>trong&gt;OfficeAid AS, organisasjonsnummer 912503259 er ansvarlig for behandlingen av personopplysninger og kan ved spørsmål kontaktes på post@officeaid.</pre>

### 912766349 - CUBASTOLEN AS - website

- url: `https://cubastolen.no`
- proof tier: `orgnr_on_page`
- identity level: `VERIFIED`
- automated verdict: **correct**

Source: https://cubastolen.no/pages/kjops-og-leveringsvilkar

Retrieved: 2026-11-17T17:31:52.985647Z; SHA-256 `99fb2ea5c23664c225244f75634b910606a8618e58d986dfd3b9b2ce42066300`; locator `identity-proof:912766349`; method `signalpost.website.v1`.

<pre>data-start="475" data-end="478"&gt;Org.nr: 912 766 349&lt;br data-start="497" data-end="500"&gt;Del av Staas AS&lt;br data-start="515" data-end="518"&gt;Adresse: Hes</pre>

### 913112245 - TANKESMIEN AGENDA AS - website

- url: `https://www.tankesmienagenda.no`
- proof tier: `orgnr_on_page`
- identity level: `VERIFIED`
- automated verdict: **correct**

Source: https://www.tankesmienagenda.no/kontakt-oss

Retrieved: 2026-11-17T17:34:49.349896Z; SHA-256 `e76a4989c1695f2f0a3acb958494cd1d35b1702c2e2d8f0d7eab2257c2d0f296`; locator `identity-proof:913112245`; method `signalpost.website.v1`.

<pre>mer&lt;/h3&gt;&lt;p class="mb-[0.9em] last:mb-0"&gt;913 112 245&lt;/p&gt;&lt;p class="mb-[0.9em] last:mb-0"&gt;Vi motter faktura som EHF-faktura eller på e-post.&lt;/p&gt;&lt;/div&gt;&lt;/d</pre>

Source: https://www.tankesmienagenda.no/kontakt-oss

Retrieved: 2026-11-17T17:34:49.349896Z; SHA-256 `e76a4989c1695f2f0a3acb958494cd1d35b1702c2e2d8f0d7eab2257c2d0f296`; locator `registry-contact:email_domain`; method `signalpost.registry_contact.v1`.

<pre>&lt;a href="mailto:post@tankesmienagenda.no" rel="noreferrer" class="group inline-flex items-center gap-x-[0.2em]"&gt;</pre>

### 914848962 - TRYKKEBRAKKA AS - website

- url: `https://trykkebrakka.no`
- proof tier: `orgnr_on_page`
- identity level: `VERIFIED`
- automated verdict: **correct**

Source: https://trykkebrakka.no/

Retrieved: 2026-11-17T17:36:14.399319Z; SHA-256 `5d8248beec77dfe8ae0acd675d97d145e0c6fe333c7409e8f64df518e28bad9b`; locator `identity-proof:914848962`; method `signalpost.website.v1`.

<pre> rte"&gt;
                      &lt;p&gt;Org nr: 914 848 962&lt;/p&gt;&lt;p&gt;Skoglivegen 23, 3539 Flå&lt;/p&gt;&lt;p&gt;trykkebrakka@gmail.com&lt;/p&gt;
                    &lt;/div&gt;&lt;/div&gt;&lt;/</pre>

### 916364806 - TT EXPRESS AS - website

- url: `https://www.ttexpress.no`
- proof tier: `orgnr_on_page`
- identity level: `VERIFIED`
- automated verdict: **correct**

Source: https://www.ttexpress.no/

Retrieved: 2026-11-17T17:34:46.072576Z; SHA-256 `9e61edce2a822ed1a26c3244913a2719b70e5ccca16b28c03b74cdd9e901365d`; locator `identity-proof:916364806`; method `signalpost.website.v1`.

<pre>     &lt;small&gt;Organisasjonsnummer&lt;/small&gt;
916364806
                        
                    &lt;/div&gt;

                &lt;/div&gt;
            &lt;/div&gt;
     </pre>

### 916667779 - PRESENZA AS - website

- url: `https://presenza.no`
- proof tier: `orgnr_on_page`
- identity level: `VERIFIED`
- automated verdict: **correct**

Source: https://presenza.no/

Retrieved: 2026-11-17T17:34:24.393136Z; SHA-256 `96a5ee7318ff61117673620704ec04cfcea8f6d117e5c1ac76d4a2ef454edcbb`; locator `identity-proof:916667779`; method `signalpost.website.v1`.

<pre>no&lt;/a&gt;&lt;br /&gt;&lt;strong&gt;Orgnummer:&lt;/strong&gt; 916667779MVA&lt;/p&gt;
&lt;p&gt;&lt;span style="text-decoration: underline;"&gt;&lt;strong&gt;&lt;a href="https://presenza.no/personverne</pre>

### 918307613 - DYBWADSGYNEKOLOGENE DA - website

- url: `https://dybwadsgynekologene.no`
- proof tier: `orgnr_on_page`
- identity level: `VERIFIED`
- automated verdict: **correct**

Source: https://dybwadsgynekologene.no/

Retrieved: 2026-11-17T17:32:33.475006Z; SHA-256 `116f6fcf41757ddd74b8c5da2a3ea89ce2010e049e89afc293ed85bd9506294d`; locator `identity-proof:918307613`; method `signalpost.website.v1`.

<pre>026 Dybwadsgynekologene&lt;/p&gt; &lt;p&gt;Org. nr. 918 307 613&lt;/p&gt; &lt;/div&gt; &lt;/div&gt; &lt;/footer&gt; &lt;script&gt;
            (() =&gt; {
            const getTheme = () =&gt;
     </pre>

Source: https://dybwadsgynekologene.no/

Retrieved: 2026-11-17T17:32:33.475006Z; SHA-256 `116f6fcf41757ddd74b8c5da2a3ea89ce2010e049e89afc293ed85bd9506294d`; locator `registry-contact:phone`; method `signalpost.registry_contact.v1`.

<pre>&lt;a href="tel:22926092" class="underline-offset-4 hover:underline"&gt;</pre>

### 918978488 - SVOLT AS - website

- url: `https://www.svolt.no`
- proof tier: `orgnr_on_page`
- identity level: `VERIFIED`
- automated verdict: **correct**

Source: https://www.svolt.no/

Retrieved: 2026-11-17T17:36:22.129099Z; SHA-256 `7f63abdb2df0e4e7caffe5874962f099191ed59a686c446bfca7fe848f9f77d9`; locator `identity-proof:918978488`; method `signalpost.website.v1`.

<pre>3 TRONDHEIM&lt;/p&gt;
&lt;p&gt;Organisasjonsnummer: 918 978 488&lt;/p&gt;
&lt;/div&gt;
&lt;/div&gt;&lt;/div&gt;&lt;/div&gt;&lt;div id="pgc-14-4-1"  class="panel-grid-cell" &gt;&lt;div id="panel-14-4-1-</pre>

### 920153577 - ELMERA GROUP ASA - website

- url: `https://elmeragroup.no`
- proof tier: `orgnr_on_page`
- identity level: `VERIFIED`
- automated verdict: **correct**

Source: https://elmeragroup.no/

Retrieved: 2026-11-17T17:36:15.570732Z; SHA-256 `90152513e946c49b7213093211992d8c36061c4dd0bf098f878e43572e4009e5`; locator `identity-proof:920153577`; method `signalpost.website.v1`.

<pre>  &lt;p&gt;&lt;strong&gt;Org.nr&lt;br /&gt;&lt;/strong&gt;&lt;span&gt;920 153 577&lt;/span&gt;&lt;/p&gt;
                &lt;/div&gt;
                &lt;div class="column"&gt;
                    
  </pre>

### 922157324 - THERESE ENGER AS - website

- url: `https://www.thereseenger.no`
- proof tier: `jsonld_vatid`
- identity level: `VERIFIED`
- automated verdict: **correct**

Source: https://www.thereseenger.no/

Retrieved: 2026-11-17T17:33:32.047872Z; SHA-256 `3ab24b5ff427311f2e47e64206d3750a7d49dfe9309873c5da08d8a502d2605d`; locator `identity-proof:922157324`; method `signalpost.website.v1`.

<pre>s?cid=16328723874553620968"],"vatID":"NO922157324MVA","identifier":{"@type":"PropertyValue","propertyID":"Norwegian organisation number","value":"9221</pre>

### 923240942 - ONLYNX AS - website

- url: `https://onlynx.no`
- proof tier: `orgnr_on_page`
- identity level: `VERIFIED`
- automated verdict: **correct**

Source: https://onlynx.no/personvern

Retrieved: 2026-11-17T17:35:38.667004Z; SHA-256 `877fbb1756497483d3d0f165e7dd384fb905d8ecf98d76f9e86de9c57d030456`; locator `identity-proof:923240942`; method `signalpost.website.v1`.

<pre>2&gt;&lt;p&gt;Onlynx AS&lt;!-- --&gt; (org.nr. &lt;!-- --&gt;923240942&lt;!-- --&gt;), &lt;!-- --&gt;Kristiansand, Agder&lt;!-- --&gt;, er ansvarlig for behandlingen av personopplysninger p</pre>

### 923833706 - LYSNA AS - website

- url: `https://lysna.no`
- proof tier: `orgnr_on_page`
- identity level: `VERIFIED`
- automated verdict: **correct**

Source: https://lysna.no/

Retrieved: 2026-11-17T17:35:03.108875Z; SHA-256 `533dd45facca7720480d3ba8f0472472cef379e5d7d85a8ea92aa4cac05cc781`; locator `identity-proof:923833706`; method `signalpost.website.v1`.

<pre>br /&gt;Org.nr.:&lt;/strong&gt;&lt;strong&gt; &lt;/strong&gt;923 833 706 MVA&lt;strong&gt;&lt;br /&gt;Bankgiro&lt;/strong&gt;:&lt;strong&gt; &lt;/strong&gt;&lt;span dir="ltr"&gt;1506.87.40700&lt;/span&gt;&lt;/p&gt;
    </pre>

Source: https://lysna.no/

Retrieved: 2026-11-17T17:35:03.108875Z; SHA-256 `533dd45facca7720480d3ba8f0472472cef379e5d7d85a8ea92aa4cac05cc781`; locator `registry-contact:email_domain`; method `signalpost.registry_contact.v1`.

<pre>strong&gt;&lt;/p&gt;
&lt;p&gt;&lt;strong&gt;E-post: &lt;/strong&gt;support@lysna.no&lt;strong&gt;&lt;br /&gt;Org.nr.:&lt;/strong&gt;&lt;strong&gt; &lt;/strong&gt;923 833 706 MVA&lt;strong&gt;&lt;br /&gt;Bankgiro&lt;/strong&gt;:&lt;strong&gt; &lt;/strong&gt;&lt;span dir="ltr"&gt;1506.87.40700&lt;/span&gt;&lt;/p&gt;
                                    &lt;/div&gt;
                                              </pre>

### 925757616 - BOLIGENTREPRENØREN AS - website

- url: `https://www.boligentreprenoren.no`
- proof tier: `orgnr_on_page`
- identity level: `VERIFIED`
- automated verdict: **correct**

Source: https://www.boligentreprenoren.no/

Retrieved: 2026-11-17T17:36:04.873402Z; SHA-256 `345c5fb614cc14a5408083931a5213dfe51318cd3cf1c0b5071cbadac172d6b4`; locator `identity-proof:925757616`; method `signalpost.website.v1`.

<pre>content__content"&gt;&lt;div&gt;&lt;p&gt;Orgnummer:&lt;br&gt;925 757 616&lt;br&gt;&lt;br&gt;Adresse: &lt;br&gt;Gregorius Dagssons gate 227,&lt;br&gt;3712 Skien,&lt;br&gt;Telemark&lt;br&gt;&lt;br&gt;Medlem av Nordi</pre>

### 927525399 - WOODWORKS! CLUSTER - website

- url: `https://woodworkscluster.no`
- proof tier: `orgnr_on_page`
- identity level: `VERIFIED`
- automated verdict: **correct**

Source: https://woodworkscluster.no/

Retrieved: 2026-11-17T17:31:45.682612Z; SHA-256 `8e2c2eed3e3549b40dde5c22acd82eaedef946c7e8310918f415d092e369af44`; locator `identity-proof:927525399`; method `signalpost.website.v1`.

<pre>egata 22, 7713 Steinkjer&lt;/p&gt;
&lt;p&gt;Org.nr: 927 525 399&lt;/p&gt;
&lt;p&gt;&lt;a title="Klikk for å lese personvernerklæringen til denne nettsiden" href="https://woodwor</pre>

Source: https://woodworkscluster.no/

Retrieved: 2026-11-17T17:31:45.682612Z; SHA-256 `8e2c2eed3e3549b40dde5c22acd82eaedef946c7e8310918f415d092e369af44`; locator `registry-contact:phone`; method `signalpost.registry_contact.v1`.

<pre>&lt;a title="Ring oss på telefon +47 95 23 90 06" href="tel:+47 95 23 90 06"&gt;</pre>

Source: https://woodworkscluster.no/

Retrieved: 2026-11-17T17:31:45.682612Z; SHA-256 `8e2c2eed3e3549b40dde5c22acd82eaedef946c7e8310918f415d092e369af44`; locator `registry-contact:email_domain`; method `signalpost.registry_contact.v1`.

<pre>&lt;a title="Send e-post til post@woodworkscluster.no" href="mailto:post@woodworkscluster.no"&gt;</pre>

### 929086627 - ÅLESUND BILSALG AS - website

- url: `https://alesundbilsalg.no`
- proof tier: `orgnr_on_page`
- identity level: `VERIFIED`
- automated verdict: **correct**

Source: https://alesundbilsalg.no/

Retrieved: 2026-11-17T17:32:32.577178Z; SHA-256 `1c8083d15aaefbf91de84cd1627f7ac60c584322ad5438767d2d2492c7240dbf`; locator `identity-proof:929086627`; method `signalpost.website.v1`.

<pre>pan&gt;© 2026 Ålesund Bilsalg AS · Org.nr. 929 086 627&lt;/span&gt;
      &lt;span&gt;&lt;a href="https://alesundbilsalg.no/personvern/"&gt;Personvern og informasjonskapsl</pre>

### 929274490 - BAREKNIPS AS - website

- url: `https://www.bareknips.no`
- proof tier: `orgnr_on_page`
- identity level: `VERIFIED`
- automated verdict: **correct**

Source: https://www.bareknips.no/

Retrieved: 2026-11-17T17:32:54.853696Z; SHA-256 `3b9fc590fee7e96ebf8f1f953605a0c0668a6745e23e89a0df368824b18ae28f`; locator `identity-proof:929274490`; method `signalpost.website.v1`.

<pre>7&lt;br /&gt;9405 Harstad&lt;/p&gt;
&lt;p&gt;Org nr &lt;span&gt;929 274 490&lt;/span&gt;&lt;/p&gt;
&lt;p&gt;Espen 90 72 92 57&lt;br /&gt;&lt;a href="mailto:espen@bareknips.no"&gt;espen@bareknips.no&lt;/a&gt;&lt;/p</pre>

### 932166127 - SANDAKER-NIELSEN AS - website

- url: `https://www.sandaker-nielsen.no`
- proof tier: `orgnr_on_page`
- identity level: `VERIFIED`
- automated verdict: **correct**

Source: https://www.sandaker-nielsen.no/

Retrieved: 2026-11-17T17:35:46.683739Z; SHA-256 `8fe22f52ca51c524485261abaed766f504f5dcc7a76026951e31b9c51adde465`; locator `identity-proof:932166127`; method `signalpost.website.v1`.

<pre>t-block-3"&gt;Sandaker-Nielsen AS |Org.nr. 932 166 127&lt;br/&gt;&lt;/div&gt;&lt;/div&gt;&lt;/div&gt;&lt;script src="https://d3e54v103j8qbb.cloudfront.net/js/jquery-3.5.1.min.dc5e7</pre>

### 933016196 - STEMEK AS - website

- url: `https://stemek.no`
- proof tier: `orgnr_on_page`
- identity level: `VERIFIED`
- automated verdict: **correct**

Source: https://stemek.no/

Retrieved: 2026-11-17T17:34:06.789701Z; SHA-256 `cf714e7da2e34535b5c6fd4362d75d2853248fefefe237465b17341127df94a6`; locator `identity-proof:933016196`; method `signalpost.website.v1`.

<pre>
      &lt;span&gt;© 2026 Stemek AS · Org.nr. 933 016 196&lt;/span&gt;
      &lt;span&gt;Designet av &lt;a href="https://mercatur.no" style="color:var(--brand-orange)"&gt;Mer</pre>

### 935021006 - WIIK UP CALL AS - website

- url: `https://www.wiikupcall.com`
- proof tier: `orgnr_on_page`
- identity level: `VERIFIED`
- automated verdict: **correct**

Source: https://www.wiikupcall.com/

Retrieved: 2026-11-17T17:32:02.060809Z; SHA-256 `25f88af1d5d30a98dcb8146a6c93e2186860bd547246fcc1a93a510bdf70ae24`; locator `identity-proof:935021006`; method `signalpost.website.v1`.

<pre>rong&gt;Wiik Up Call AS&lt;/strong&gt; | Org.nr: 935 021 006&lt;/p&gt;
  &lt;p&gt;Meri Wiik • &lt;a href="mailto:meri@wiikupcall.com" style="color: #e31d93;"&gt;meri@wiikupcall.</pre>

### 935219442 - EMALIE AS - website

- url: `https://emalie.no`
- proof tier: `orgnr_on_page`
- identity level: `VERIFIED`
- automated verdict: **correct**

Source: https://emalie.no/policies/terms-of-service

Retrieved: 2026-11-17T17:32:25.278449Z; SHA-256 `8cfb6aac0e9c16545cbd11b73ab9c2890867428cde9aad8610d432e128e93c8a`; locator `identity-proof:935219442`; method `signalpost.website.v1`.

<pre>gås det avtale mellom selger Emalie AS (935 219 442) og deg som kjøper.&lt;/p&gt;
&lt;p&gt;Bindende kjøpsavtale kan kun inngås med personer over 15 år, og det kan</pre>

### 967484881 - MAJAS BAKERI AS - website

- url: `https://www.majasbakeri.no`
- proof tier: `orgnr_on_page`
- identity level: `VERIFIED`
- automated verdict: **correct**

Source: https://www.majasbakeri.no/

Retrieved: 2026-11-17T17:34:03.005456Z; SHA-256 `5845372c04bcec3fcc32a73b002a669fe838e861a52664c672b385b10503116e`; locator `identity-proof:967484881`; method `signalpost.website.v1`.

<pre>pace&lt;/a&gt; | © Majas Bakeri AS - Org. nr. 967 484 881&lt;/p&gt;&lt;/p&gt;&lt;/div&gt;&lt;/div&gt;&lt;/section&gt;&lt;/footer&gt;&lt;style&gt;/* common style */

@media (min-width: 576px) {
    .</pre>

Source: https://www.majasbakeri.no/

Retrieved: 2026-11-17T17:34:03.005456Z; SHA-256 `5845372c04bcec3fcc32a73b002a669fe838e861a52664c672b385b10503116e`; locator `registry-contact:phone`; method `signalpost.registry_contact.v1`.

<pre>&lt;a href="tel:33 18 27 75" target="_blank"&gt;</pre>

Source: https://www.majasbakeri.no/

Retrieved: 2026-11-17T17:34:03.005456Z; SHA-256 `5845372c04bcec3fcc32a73b002a669fe838e861a52664c672b385b10503116e`; locator `registry-contact:email_domain`; method `signalpost.registry_contact.v1`.

<pre>&lt;a href="mailto:konditori@majasbakeri.no" target="_blank"&gt;</pre>

### 970351515 - GRANLY STIFTELSE - website

- url: `https://www.granly-stiftelse.no`
- proof tier: `orgnr_on_page`
- identity level: `VERIFIED`
- automated verdict: **correct**

Source: https://www.granly-stiftelse.no/personvernerklaering/

Retrieved: 2026-11-17T17:33:55.462009Z; SHA-256 `14bd9ca90547097dbd93082d7a351e9be24f4bea7f9c4c25cd7a034dbb74d5f1`; locator `identity-proof:970351515`; method `signalpost.website.v1`.

<pre>r /&gt;
Telefon: 61 14 36 60&lt;br /&gt;
Org.nr: 970 351 515&lt;/p&gt;
&lt;p&gt;For spørsmål du måtte ha om vår behandling av dine personopplysninger kan du kontakte dagli</pre>

Source: https://www.granly-stiftelse.no/personvernerklaering/

Retrieved: 2026-11-17T17:33:55.462009Z; SHA-256 `14bd9ca90547097dbd93082d7a351e9be24f4bea7f9c4c25cd7a034dbb74d5f1`; locator `registry-contact:phone`; method `signalpost.registry_contact.v1`.

<pre>&lt;a style="color: #000000;" href="tel:+4761143660"&gt;</pre>

Source: https://www.granly-stiftelse.no/personvernerklaering/

Retrieved: 2026-11-17T17:33:55.462009Z; SHA-256 `14bd9ca90547097dbd93082d7a351e9be24f4bea7f9c4c25cd7a034dbb74d5f1`; locator `registry-contact:email_domain`; method `signalpost.registry_contact.v1`.

<pre>&lt;a style="color: #000000;" href="mailto:granly@granly-stiftelse.no"&gt;</pre>

### 975339688 - DIGERNES AS - website

- url: `https://www.digernes.no`
- proof tier: `orgnr_on_page`
- identity level: `VERIFIED`
- automated verdict: **correct**

Source: https://www.digernes.no/om-oss/pernsonvernerklaering

Retrieved: 2026-11-17T17:35:56.364412Z; SHA-256 `d8094de54dff4412a40717eaf65997b14a64c5e900e2cfd4c42bbf961c58d888`; locator `identity-proof:975339688`; method `signalpost.website.v1`.

<pre>ingsansvar&lt;/h3&gt;
&lt;p&gt;Digernes AS (Org.nr: 975 339 688) er behandlingsansvarlig for personopplysningene vi samler inn og behandler. Dette innebærer at vi</pre>

Source: https://www.digernes.no/om-oss/pernsonvernerklaering

Retrieved: 2026-11-17T17:35:56.364412Z; SHA-256 `d8094de54dff4412a40717eaf65997b14a64c5e900e2cfd4c42bbf961c58d888`; locator `registry-contact:phone`; method `signalpost.registry_contact.v1`.

<pre>&lt;a href="tel:4751779898"&gt;</pre>

### 983100147 - VASSFARBYGG AS - website

- url: `https://vassfarbygg.no`
- proof tier: `orgnr_on_page`
- identity level: `VERIFIED`
- automated verdict: **correct**

Source: https://vassfarbygg.no/

Retrieved: 2026-11-17T17:34:17.978957Z; SHA-256 `888dd9525ed8f48418dc54b682f150d32167dcd7cc93a27c8221a4201ced2bac`; locator `identity-proof:983100147`; method `signalpost.website.v1`.

<pre>;&lt;span id="span-426-9" class="ct-span" &gt;983100147&lt;/span&gt;&lt;/div&gt;&lt;/div&gt;&lt;/div&gt;&lt;div id="div_block-386-9" class="ct-div-block footer-some-content" &gt;&lt;/div&gt;&lt;d</pre>

### 985256055 - FRAMEWORKS AS - website

- url: `https://frameworks.no`
- proof tier: `orgnr_on_page`
- identity level: `VERIFIED`
- automated verdict: **correct**

Source: https://frameworks.no/

Retrieved: 2026-11-17T17:35:33.256098Z; SHA-256 `09a6f3b7ec8bab0877adfa3b7d56e15bd2693b782ec14d9e8ccabeb9d90d4cfe`; locator `identity-proof:985256055`; method `signalpost.website.v1`.

<pre>den 2012. Organisasjonsnummeret vårt er 985 256 055. Du når oss på telefon &lt;a href="tel:+4740400088"&gt;40 40 00 88&lt;/a&gt; eller på &lt;a href="mailto:simen.wi</pre>

Source: https://frameworks.no/

Retrieved: 2026-11-17T17:35:33.256098Z; SHA-256 `09a6f3b7ec8bab0877adfa3b7d56e15bd2693b782ec14d9e8ccabeb9d90d4cfe`; locator `registry-contact:email_domain`; method `signalpost.registry_contact.v1`.

<pre>&lt;a href="mailto:sw@frameworks.no" target="_self" class="e-paragraph-link-base e-default-a"&gt;</pre>

### 987693444 - ET BYGG AS - website

- url: `https://etbygg.com`
- proof tier: `orgnr_on_page`
- identity level: `VERIFIED`
- automated verdict: **correct**

Source: https://etbygg.com/

Retrieved: 2026-11-17T17:33:52.591267Z; SHA-256 `39840b221fae64efea13dfd02ba688fd6a81158f89e66b148c327d77df925c74`; locator `identity-proof:987693444`; method `signalpost.website.v1`.

<pre>&gt; ET Bygg AS&lt;/span&gt;
      &lt;span&gt;Org.nr. 987 693 444&lt;/span&gt;
      &lt;span&gt;Medlem av Mesterhus&lt;/span&gt;
      &lt;!-- Vilkaarslenkene skyves bort fra selskapso</pre>

### 987747218 - XRGIA AS - website

- url: `https://xrgia.no`
- proof tier: `orgnr_on_page`
- identity level: `VERIFIED`
- automated verdict: **correct**

Source: https://xrgia.no/

Retrieved: 2026-11-17T17:34:11.584298Z; SHA-256 `730a39c7bc29e8b6525186c4546858234ef27f22173d94cb0ea9a2e400f86045`; locator `identity-proof:987747218`; method `signalpost.website.v1`.

<pre>845&lt;/a&gt;&lt;br /&gt;
&lt;strong&gt;Org. nr:&lt;/strong&gt; 987 747 218 MVA&lt;/p&gt;
&lt;/div&gt;
		&lt;span class="seperator extralight-border"&gt;&lt;/span&gt;&lt;/section&gt;&lt;/div&gt;&lt;div class='flex</pre>

Source: https://xrgia.no/

Retrieved: 2026-11-17T17:34:11.584298Z; SHA-256 `730a39c7bc29e8b6525186c4546858234ef27f22173d94cb0ea9a2e400f86045`; locator `registry-contact:email_domain`; method `signalpost.registry_contact.v1`.

<pre>&lt;a href="&amp;#x6d;&amp;#x61;&amp;#x69;&amp;#108;&amp;#116;o:&amp;#x74;&amp;#x6f;&amp;#x6d;&amp;#109;&amp;#121;&amp;#64;x&amp;#x72;&amp;#x67;&amp;#x69;&amp;#97;&amp;#46;no"&gt;</pre>

### 988481580 - REVISORSENTERET MANDAL AS - website

- url: `https://revisorsenteretmandal.no`
- proof tier: `orgnr_on_page`
- identity level: `VERIFIED`
- automated verdict: **correct**

Source: https://revisorsenteretmandal.no/

Retrieved: 2026-11-17T17:33:51.233929Z; SHA-256 `7ad6a77fbf7c22f2d7fbfa95e21fb701a8e74d29ce3474b23dd7461b899965e9`; locator `identity-proof:988481580`; method `signalpost.website.v1`.

<pre> 13h7M8.5 16.5h5"/&gt;&lt;/svg&gt; &lt;span&gt;Org.nr. 988 481 580&lt;/span&gt; &lt;/li&gt; &lt;/ul&gt; &lt;/div&gt; &lt;/div&gt; &lt;div class="border-t border-white/10"&gt; &lt;div class="container flex</pre>

### 990024545 - TORGERSEN BIL AS - website

- url: `https://torgersenbil.no`
- proof tier: `jsonld_vatid`
- identity level: `VERIFIED`
- automated verdict: **correct**

Source: https://torgersenbil.no/

Retrieved: 2026-11-17T17:35:28.827795Z; SHA-256 `fdbfc4082666e6babdc917d099212ccce7f54a894d9ee6ab1b19faafe370eecc`; locator `identity-proof:990024545`; method `signalpost.website.v1`.

<pre>nized-list__content" itemprop="vatID"&gt;NO990024545 MVA&lt;/dd&gt;
    
    &lt;dt class="hide"&gt;Theme primary color&lt;/dt&gt;
    &lt;dd class="hide" itemprop="additiona</pre>

### 991625216 - SONO NORGE AS - website

- url: `https://www.sono.no`
- proof tier: `orgnr_on_page`
- identity level: `VERIFIED`
- automated verdict: **correct**

Source: https://www.sono.no/

Retrieved: 2026-11-17T17:34:50.045909Z; SHA-256 `f9b887a7f5a49f51ea6fe0cf108c29eeb360744081d2759bf359961a301093e3`; locator `identity-proof:991625216`; method `signalpost.website.v1`.

<pre>en &lt;br&gt;
                        Org.nr: 991 625 216                    &lt;/div&gt;
                &lt;/div&gt;
            &lt;/div&gt;
        &lt;/div&gt;
    &lt;/div&gt;
    </pre>

### 991979514 - SCANLIFT AS - website

- url: `https://scanlift.no`
- proof tier: `orgnr_on_page`
- identity level: `VERIFIED`
- automated verdict: **correct**

Source: https://scanlift.no/

Retrieved: 2026-11-17T17:35:07.609903Z; SHA-256 `a6a57f7a0a3b933465138dc2ac9b6726213efba63cc072329664f37c190b1eba`; locator `identity-proof:991979514`; method `signalpost.website.v1`.

<pre>26 © &lt;strong&gt;Scanlift as&lt;/strong&gt;
Org # 991979514 MVA&lt;/div&gt;&lt;/div&gt;&lt;/div&gt;&lt;/div&gt;
&lt;button
type=button id=top-link class="back-to-top button icon invert pl</pre>

### 994479865 - IDENTUM AS - website

- url: `https://www.identum.no`
- proof tier: `orgnr_on_page`
- identity level: `VERIFIED`
- automated verdict: **correct**

Source: https://www.identum.no/

Retrieved: 2026-11-17T17:32:01.564168Z; SHA-256 `356223741f48deba792eff2c569e1b2a0b4bdee0c59d567e77912eb72e1301d0`; locator `identity-proof:994479865`; method `signalpost.website.v1`.

<pre>"&gt;Organisasjonsnummer&lt;/h3&gt;
        &lt;p&gt;NO994479865 MVA&lt;/p&gt;
      &lt;/li&gt;
    
    &lt;/ul&gt;
  
&lt;/div&gt;
&lt;/div&gt;
        
      &lt;/div&gt;
      &lt;div class="footer-i</pre>

### 997963148 - VERDI WEB AS - website

- url: `https://verdiweb.no`
- proof tier: `jsonld_vatid`
- identity level: `VERIFIED`
- automated verdict: **correct**

Source: https://verdiweb.no/

Retrieved: 2026-11-17T17:35:55.415365Z; SHA-256 `dc59cb69cb09cdbf5ccfaf53d6ce26d2da0c41854a5c6e3c3a25ee0625d69cdf`; locator `identity-proof:997963148`; method `signalpost.website.v1`.

<pre>ray-500 text-sm"&gt;Verdi Web AS &amp;middot; Org.nr. 997 963 148&lt;/div&gt;&lt;/div&gt;&lt;div&gt;&lt;form id="contact-form" class="space-y-5"&gt;&lt;div&gt;&lt;label for="contact-name" cl</pre>

Source: https://verdiweb.no/

Retrieved: 2026-11-17T17:35:55.415365Z; SHA-256 `dc59cb69cb09cdbf5ccfaf53d6ce26d2da0c41854a5c6e3c3a25ee0625d69cdf`; locator `registry-contact:email_domain`; method `signalpost.registry_contact.v1`.

<pre>ikkerhet og langsiktig verdi.","email":"post@verdiweb.no","identifier":{"@type":"PropertyValue","name":"Organisasjonsnummer","value":"997963148"},"address":{"@type":"PostalAddress","addressCountry":"NO"},"areaServed":{"@type":"Country","name":"Norway"},"knowsLanguage":["nb","en"],"serviceType":["Web</pre>

## Social — automated correct (20)

### 912766349 - CUBASTOLEN AS - social

- url: `https://www.facebook.com/cubastolen`
- proof tier: `own_header_footer_exact_name_v1`
- automated verdict: **correct**

Source: https://cubastolen.no/

Retrieved: 2026-11-17T17:31:50.465986Z; SHA-256 `5c5c968dd71032d68f510cbf119082f4f93a6c9b4db2e79970eba9bb6a2214b5`; locator `company-link:https://www.facebook.com/cubastolen`; method `signalpost.website.v1`.

<pre>&lt;a target="_blank" rel="noopener" href="https://www.facebook.com/cubastolen" title=""&gt;</pre>

Source: https://cubastolen.no/pages/kjops-og-leveringsvilkar

Retrieved: 2026-11-17T17:31:52.985647Z; SHA-256 `99fb2ea5c23664c225244f75634b910606a8618e58d986dfd3b9b2ce42066300`; locator `identity-proof:912766349`; method `signalpost.website.v1`.

<pre>data-start="475" data-end="478"&gt;Org.nr: 912 766 349&lt;br data-start="497" data-end="500"&gt;Del av Staas AS&lt;br data-start="515" data-end="518"&gt;Adresse: Hes</pre>

### 913112245 - TANKESMIEN AGENDA AS - social

- url: `https://www.facebook.com/tankesmienagenda`
- proof tier: `own_header_footer_exact_name_v1`
- automated verdict: **correct**

Source: https://www.tankesmienagenda.no/

Retrieved: 2026-11-17T17:34:47.625041Z; SHA-256 `5bfb71cd7b851a28dc49c8c519c995306e494e8eaa208bcddf431f34d0c4fade`; locator `company-link:https://www.facebook.com/tankesmienagenda`; method `signalpost.website.v1`.

<pre>&lt;a href="https://www.facebook.com/tankesmienagenda" rel="noreferrer" class="group inline-flex items-center gap-x-[0.2em]"&gt;</pre>

Source: https://www.tankesmienagenda.no/kontakt-oss

Retrieved: 2026-11-17T17:34:49.349896Z; SHA-256 `e76a4989c1695f2f0a3acb958494cd1d35b1702c2e2d8f0d7eab2257c2d0f296`; locator `identity-proof:913112245`; method `signalpost.website.v1`.

<pre>mer&lt;/h3&gt;&lt;p class="mb-[0.9em] last:mb-0"&gt;913 112 245&lt;/p&gt;&lt;p class="mb-[0.9em] last:mb-0"&gt;Vi motter faktura som EHF-faktura eller på e-post.&lt;/p&gt;&lt;/div&gt;&lt;/d</pre>

Source: https://www.tankesmienagenda.no/kontakt-oss

Retrieved: 2026-11-17T17:34:49.349896Z; SHA-256 `e76a4989c1695f2f0a3acb958494cd1d35b1702c2e2d8f0d7eab2257c2d0f296`; locator `registry-contact:email_domain`; method `signalpost.registry_contact.v1`.

<pre>&lt;a href="mailto:post@tankesmienagenda.no" rel="noreferrer" class="group inline-flex items-center gap-x-[0.2em]"&gt;</pre>

### 913112245 - TANKESMIEN AGENDA AS - social

- url: `https://www.instagram.com/tankesmien_agenda`
- proof tier: `own_header_footer_exact_name_v1`
- automated verdict: **correct**

Source: https://www.tankesmienagenda.no/

Retrieved: 2026-11-17T17:34:47.625041Z; SHA-256 `5bfb71cd7b851a28dc49c8c519c995306e494e8eaa208bcddf431f34d0c4fade`; locator `company-link:https://www.instagram.com/tankesmien_agenda`; method `signalpost.website.v1`.

<pre>&lt;a href="https://www.instagram.com/tankesmien_agenda" rel="noreferrer" class="group inline-flex items-center gap-x-[0.2em]"&gt;</pre>

Source: https://www.tankesmienagenda.no/kontakt-oss

Retrieved: 2026-11-17T17:34:49.349896Z; SHA-256 `e76a4989c1695f2f0a3acb958494cd1d35b1702c2e2d8f0d7eab2257c2d0f296`; locator `identity-proof:913112245`; method `signalpost.website.v1`.

<pre>mer&lt;/h3&gt;&lt;p class="mb-[0.9em] last:mb-0"&gt;913 112 245&lt;/p&gt;&lt;p class="mb-[0.9em] last:mb-0"&gt;Vi motter faktura som EHF-faktura eller på e-post.&lt;/p&gt;&lt;/div&gt;&lt;/d</pre>

Source: https://www.tankesmienagenda.no/kontakt-oss

Retrieved: 2026-11-17T17:34:49.349896Z; SHA-256 `e76a4989c1695f2f0a3acb958494cd1d35b1702c2e2d8f0d7eab2257c2d0f296`; locator `registry-contact:email_domain`; method `signalpost.registry_contact.v1`.

<pre>&lt;a href="mailto:post@tankesmienagenda.no" rel="noreferrer" class="group inline-flex items-center gap-x-[0.2em]"&gt;</pre>

### 913112245 - TANKESMIEN AGENDA AS - social

- url: `https://www.linkedin.com/company/tankesmien-agenda`
- proof tier: `own_header_footer_exact_name_v1`
- automated verdict: **correct**

Source: https://www.tankesmienagenda.no/

Retrieved: 2026-11-17T17:34:47.625041Z; SHA-256 `5bfb71cd7b851a28dc49c8c519c995306e494e8eaa208bcddf431f34d0c4fade`; locator `company-link:https://www.linkedin.com/company/tankesmien-agenda`; method `signalpost.website.v1`.

<pre>&lt;a href="https://www.linkedin.com/company/tankesmien-agenda/" rel="noreferrer" class="group inline-flex items-center gap-x-[0.2em]"&gt;</pre>

Source: https://www.tankesmienagenda.no/kontakt-oss

Retrieved: 2026-11-17T17:34:49.349896Z; SHA-256 `e76a4989c1695f2f0a3acb958494cd1d35b1702c2e2d8f0d7eab2257c2d0f296`; locator `identity-proof:913112245`; method `signalpost.website.v1`.

<pre>mer&lt;/h3&gt;&lt;p class="mb-[0.9em] last:mb-0"&gt;913 112 245&lt;/p&gt;&lt;p class="mb-[0.9em] last:mb-0"&gt;Vi motter faktura som EHF-faktura eller på e-post.&lt;/p&gt;&lt;/div&gt;&lt;/d</pre>

Source: https://www.tankesmienagenda.no/kontakt-oss

Retrieved: 2026-11-17T17:34:49.349896Z; SHA-256 `e76a4989c1695f2f0a3acb958494cd1d35b1702c2e2d8f0d7eab2257c2d0f296`; locator `registry-contact:email_domain`; method `signalpost.registry_contact.v1`.

<pre>&lt;a href="mailto:post@tankesmienagenda.no" rel="noreferrer" class="group inline-flex items-center gap-x-[0.2em]"&gt;</pre>

### 913112245 - TANKESMIEN AGENDA AS - social

- url: `https://www.tiktok.com/@tankesmien.agenda`
- proof tier: `own_header_footer_exact_name_v1`
- automated verdict: **correct**

Source: https://www.tankesmienagenda.no/

Retrieved: 2026-11-17T17:34:47.625041Z; SHA-256 `5bfb71cd7b851a28dc49c8c519c995306e494e8eaa208bcddf431f34d0c4fade`; locator `company-link:https://www.tiktok.com/@tankesmien.agenda`; method `signalpost.website.v1`.

<pre>&lt;a href="https://www.tiktok.com/@tankesmien.agenda?is_from_webapp=1&amp;amp;sender_device=pc" rel="noreferrer" class="group inline-flex items-center gap-x-[0.2em]"&gt;</pre>

Source: https://www.tankesmienagenda.no/kontakt-oss

Retrieved: 2026-11-17T17:34:49.349896Z; SHA-256 `e76a4989c1695f2f0a3acb958494cd1d35b1702c2e2d8f0d7eab2257c2d0f296`; locator `identity-proof:913112245`; method `signalpost.website.v1`.

<pre>mer&lt;/h3&gt;&lt;p class="mb-[0.9em] last:mb-0"&gt;913 112 245&lt;/p&gt;&lt;p class="mb-[0.9em] last:mb-0"&gt;Vi motter faktura som EHF-faktura eller på e-post.&lt;/p&gt;&lt;/div&gt;&lt;/d</pre>

Source: https://www.tankesmienagenda.no/kontakt-oss

Retrieved: 2026-11-17T17:34:49.349896Z; SHA-256 `e76a4989c1695f2f0a3acb958494cd1d35b1702c2e2d8f0d7eab2257c2d0f296`; locator `registry-contact:email_domain`; method `signalpost.registry_contact.v1`.

<pre>&lt;a href="mailto:post@tankesmienagenda.no" rel="noreferrer" class="group inline-flex items-center gap-x-[0.2em]"&gt;</pre>

### 916667779 - PRESENZA AS - social

- url: `https://www.facebook.com/PresenzaAs`
- proof tier: `own_header_footer_exact_name_v1`
- automated verdict: **correct**

Source: https://presenza.no/

Retrieved: 2026-11-17T17:34:24.393136Z; SHA-256 `96a5ee7318ff61117673620704ec04cfcea8f6d117e5c1ac76d4a2ef454edcbb`; locator `company-link:https://www.facebook.com/PresenzaAs`; method `signalpost.website.v1`.

<pre>&lt;a
              href='https://www.facebook.com/PresenzaAs'
              class='icon et_pb_with_border'
              title='Følg på Facebook'
               target="_blank"&gt;</pre>

Source: https://presenza.no/

Retrieved: 2026-11-17T17:34:24.393136Z; SHA-256 `96a5ee7318ff61117673620704ec04cfcea8f6d117e5c1ac76d4a2ef454edcbb`; locator `identity-proof:916667779`; method `signalpost.website.v1`.

<pre>no&lt;/a&gt;&lt;br /&gt;&lt;strong&gt;Orgnummer:&lt;/strong&gt; 916667779MVA&lt;/p&gt;
&lt;p&gt;&lt;span style="text-decoration: underline;"&gt;&lt;strong&gt;&lt;a href="https://presenza.no/personverne</pre>

### 925757616 - BOLIGENTREPRENØREN AS - social

- url: `https://www.facebook.com/boligentreprenorenas`
- proof tier: `own_header_footer_exact_name_v1`
- automated verdict: **correct**

Source: https://www.boligentreprenoren.no/

Retrieved: 2026-11-17T17:36:04.873402Z; SHA-256 `345c5fb614cc14a5408083931a5213dfe51318cd3cf1c0b5071cbadac172d6b4`; locator `company-link:https://www.facebook.com/boligentreprenorenas`; method `signalpost.website.v1`.

<pre>&lt;a href="https://www.facebook.com/boligentreprenorenas" rel="noopener noreferrer"&gt;</pre>

Source: https://www.boligentreprenoren.no/

Retrieved: 2026-11-17T17:36:04.873402Z; SHA-256 `345c5fb614cc14a5408083931a5213dfe51318cd3cf1c0b5071cbadac172d6b4`; locator `identity-proof:925757616`; method `signalpost.website.v1`.

<pre>content__content"&gt;&lt;div&gt;&lt;p&gt;Orgnummer:&lt;br&gt;925 757 616&lt;br&gt;&lt;br&gt;Adresse: &lt;br&gt;Gregorius Dagssons gate 227,&lt;br&gt;3712 Skien,&lt;br&gt;Telemark&lt;br&gt;&lt;br&gt;Medlem av Nordi</pre>

### 927525399 - WOODWORKS! CLUSTER - social

- url: `https://linkedin.com/company/woodworks-cluster`
- proof tier: `own_header_footer_exact_name_v1`
- automated verdict: **correct**

Source: https://woodworkscluster.no/

Retrieved: 2026-11-17T17:31:45.682612Z; SHA-256 `8e2c2eed3e3549b40dde5c22acd82eaedef946c7e8310918f415d092e369af44`; locator `company-link:https://linkedin.com/company/woodworks-cluster`; method `signalpost.website.v1`.

<pre>&lt;a href="https://linkedin.com/company/woodworks-cluster" target="_blank" rel="noopener nofollow"&gt;</pre>

Source: https://woodworkscluster.no/

Retrieved: 2026-11-17T17:31:45.682612Z; SHA-256 `8e2c2eed3e3549b40dde5c22acd82eaedef946c7e8310918f415d092e369af44`; locator `identity-proof:927525399`; method `signalpost.website.v1`.

<pre>egata 22, 7713 Steinkjer&lt;/p&gt;
&lt;p&gt;Org.nr: 927 525 399&lt;/p&gt;
&lt;p&gt;&lt;a title="Klikk for å lese personvernerklæringen til denne nettsiden" href="https://woodwor</pre>

Source: https://woodworkscluster.no/

Retrieved: 2026-11-17T17:31:45.682612Z; SHA-256 `8e2c2eed3e3549b40dde5c22acd82eaedef946c7e8310918f415d092e369af44`; locator `registry-contact:phone`; method `signalpost.registry_contact.v1`.

<pre>&lt;a title="Ring oss på telefon +47 95 23 90 06" href="tel:+47 95 23 90 06"&gt;</pre>

Source: https://woodworkscluster.no/

Retrieved: 2026-11-17T17:31:45.682612Z; SHA-256 `8e2c2eed3e3549b40dde5c22acd82eaedef946c7e8310918f415d092e369af44`; locator `registry-contact:email_domain`; method `signalpost.registry_contact.v1`.

<pre>&lt;a title="Send e-post til post@woodworkscluster.no" href="mailto:post@woodworkscluster.no"&gt;</pre>

### 927525399 - WOODWORKS! CLUSTER - social

- url: `https://www.facebook.com/woodworkscluster`
- proof tier: `own_header_footer_exact_name_v1`
- automated verdict: **correct**

Source: https://woodworkscluster.no/

Retrieved: 2026-11-17T17:31:45.682612Z; SHA-256 `8e2c2eed3e3549b40dde5c22acd82eaedef946c7e8310918f415d092e369af44`; locator `company-link:https://www.facebook.com/woodworkscluster`; method `signalpost.website.v1`.

<pre>&lt;a href="https://www.facebook.com/woodworkscluster/" target="_blank" rel="noopener nofollow"&gt;</pre>

Source: https://woodworkscluster.no/

Retrieved: 2026-11-17T17:31:45.682612Z; SHA-256 `8e2c2eed3e3549b40dde5c22acd82eaedef946c7e8310918f415d092e369af44`; locator `identity-proof:927525399`; method `signalpost.website.v1`.

<pre>egata 22, 7713 Steinkjer&lt;/p&gt;
&lt;p&gt;Org.nr: 927 525 399&lt;/p&gt;
&lt;p&gt;&lt;a title="Klikk for å lese personvernerklæringen til denne nettsiden" href="https://woodwor</pre>

Source: https://woodworkscluster.no/

Retrieved: 2026-11-17T17:31:45.682612Z; SHA-256 `8e2c2eed3e3549b40dde5c22acd82eaedef946c7e8310918f415d092e369af44`; locator `registry-contact:phone`; method `signalpost.registry_contact.v1`.

<pre>&lt;a title="Ring oss på telefon +47 95 23 90 06" href="tel:+47 95 23 90 06"&gt;</pre>

Source: https://woodworkscluster.no/

Retrieved: 2026-11-17T17:31:45.682612Z; SHA-256 `8e2c2eed3e3549b40dde5c22acd82eaedef946c7e8310918f415d092e369af44`; locator `registry-contact:email_domain`; method `signalpost.registry_contact.v1`.

<pre>&lt;a title="Send e-post til post@woodworkscluster.no" href="mailto:post@woodworkscluster.no"&gt;</pre>

### 929274490 - BAREKNIPS AS - social

- url: `https://facebook.com/bareknips`
- proof tier: `own_header_footer_exact_name_v1`
- automated verdict: **correct**

Source: https://www.bareknips.no/

Retrieved: 2026-11-17T17:32:54.853696Z; SHA-256 `3b9fc590fee7e96ebf8f1f953605a0c0668a6745e23e89a0df368824b18ae28f`; locator `company-link:https://facebook.com/bareknips`; method `signalpost.website.v1`.

<pre>&lt;a href="https://facebook.com/bareknips" target="_blank" rel="noopener"&gt;</pre>

Source: https://www.bareknips.no/

Retrieved: 2026-11-17T17:32:54.853696Z; SHA-256 `3b9fc590fee7e96ebf8f1f953605a0c0668a6745e23e89a0df368824b18ae28f`; locator `identity-proof:929274490`; method `signalpost.website.v1`.

<pre>7&lt;br /&gt;9405 Harstad&lt;/p&gt;
&lt;p&gt;Org nr &lt;span&gt;929 274 490&lt;/span&gt;&lt;/p&gt;
&lt;p&gt;Espen 90 72 92 57&lt;br /&gt;&lt;a href="mailto:espen@bareknips.no"&gt;espen@bareknips.no&lt;/a&gt;&lt;/p</pre>

### 929274490 - BAREKNIPS AS - social

- url: `https://instagram.com/bareknips`
- proof tier: `own_header_footer_exact_name_v1`
- automated verdict: **correct**

Source: https://www.bareknips.no/

Retrieved: 2026-11-17T17:32:54.853696Z; SHA-256 `3b9fc590fee7e96ebf8f1f953605a0c0668a6745e23e89a0df368824b18ae28f`; locator `company-link:https://instagram.com/bareknips`; method `signalpost.website.v1`.

<pre>&lt;a href="https://instagram.com/bareknips" target="_blank" rel="noopener"&gt;</pre>

Source: https://www.bareknips.no/

Retrieved: 2026-11-17T17:32:54.853696Z; SHA-256 `3b9fc590fee7e96ebf8f1f953605a0c0668a6745e23e89a0df368824b18ae28f`; locator `identity-proof:929274490`; method `signalpost.website.v1`.

<pre>7&lt;br /&gt;9405 Harstad&lt;/p&gt;
&lt;p&gt;Org nr &lt;span&gt;929 274 490&lt;/span&gt;&lt;/p&gt;
&lt;p&gt;Espen 90 72 92 57&lt;br /&gt;&lt;a href="mailto:espen@bareknips.no"&gt;espen@bareknips.no&lt;/a&gt;&lt;/p</pre>

### 967484881 - MAJAS BAKERI AS - social

- url: `https://www.facebook.com/MajasBakeri`
- proof tier: `own_header_footer_exact_name_v1`
- automated verdict: **correct**

Source: https://www.majasbakeri.no/

Retrieved: 2026-11-17T17:34:03.005456Z; SHA-256 `5845372c04bcec3fcc32a73b002a669fe838e861a52664c672b385b10503116e`; locator `company-link:https://www.facebook.com/MajasBakeri`; method `signalpost.website.v1`.

<pre>  " target="_blank" href="https://www.facebook.com/MajasBakeri/"&gt;</pre>

Source: https://www.majasbakeri.no/

Retrieved: 2026-11-17T17:34:03.005456Z; SHA-256 `5845372c04bcec3fcc32a73b002a669fe838e861a52664c672b385b10503116e`; locator `identity-proof:967484881`; method `signalpost.website.v1`.

<pre>pace&lt;/a&gt; | © Majas Bakeri AS - Org. nr. 967 484 881&lt;/p&gt;&lt;/p&gt;&lt;/div&gt;&lt;/div&gt;&lt;/section&gt;&lt;/footer&gt;&lt;style&gt;/* common style */

@media (min-width: 576px) {
    .</pre>

Source: https://www.majasbakeri.no/

Retrieved: 2026-11-17T17:34:03.005456Z; SHA-256 `5845372c04bcec3fcc32a73b002a669fe838e861a52664c672b385b10503116e`; locator `registry-contact:phone`; method `signalpost.registry_contact.v1`.

<pre>&lt;a href="tel:33 18 27 75" target="_blank"&gt;</pre>

Source: https://www.majasbakeri.no/

Retrieved: 2026-11-17T17:34:03.005456Z; SHA-256 `5845372c04bcec3fcc32a73b002a669fe838e861a52664c672b385b10503116e`; locator `registry-contact:email_domain`; method `signalpost.registry_contact.v1`.

<pre>&lt;a href="mailto:konditori@majasbakeri.no" target="_blank"&gt;</pre>

### 970351515 - GRANLY STIFTELSE - social

- url: `https://www.facebook.com/granlystiftelse`
- proof tier: `own_header_footer_exact_name_v1`
- automated verdict: **correct**

Source: https://www.granly-stiftelse.no/

Retrieved: 2026-11-17T17:33:51.417774Z; SHA-256 `d8cbcd495e122ee161d1f0df8ab9aeb971274e8b139c7b7eb082fc6b6b3320c6`; locator `company-link:https://www.facebook.com/granlystiftelse`; method `signalpost.website.v1`.

<pre>&lt;a href="https://www.facebook.com/granlystiftelse" &gt;</pre>

Source: https://www.granly-stiftelse.no/personvernerklaering/

Retrieved: 2026-11-17T17:33:55.462009Z; SHA-256 `14bd9ca90547097dbd93082d7a351e9be24f4bea7f9c4c25cd7a034dbb74d5f1`; locator `identity-proof:970351515`; method `signalpost.website.v1`.

<pre>r /&gt;
Telefon: 61 14 36 60&lt;br /&gt;
Org.nr: 970 351 515&lt;/p&gt;
&lt;p&gt;For spørsmål du måtte ha om vår behandling av dine personopplysninger kan du kontakte dagli</pre>

Source: https://www.granly-stiftelse.no/personvernerklaering/

Retrieved: 2026-11-17T17:33:55.462009Z; SHA-256 `14bd9ca90547097dbd93082d7a351e9be24f4bea7f9c4c25cd7a034dbb74d5f1`; locator `registry-contact:phone`; method `signalpost.registry_contact.v1`.

<pre>&lt;a style="color: #000000;" href="tel:+4761143660"&gt;</pre>

Source: https://www.granly-stiftelse.no/personvernerklaering/

Retrieved: 2026-11-17T17:33:55.462009Z; SHA-256 `14bd9ca90547097dbd93082d7a351e9be24f4bea7f9c4c25cd7a034dbb74d5f1`; locator `registry-contact:email_domain`; method `signalpost.registry_contact.v1`.

<pre>&lt;a style="color: #000000;" href="mailto:granly@granly-stiftelse.no"&gt;</pre>

### 970351515 - GRANLY STIFTELSE - social

- url: `https://www.instagram.com/granlystiftelse`
- proof tier: `own_header_footer_exact_name_v1`
- automated verdict: **correct**

Source: https://www.granly-stiftelse.no/

Retrieved: 2026-11-17T17:33:51.417774Z; SHA-256 `d8cbcd495e122ee161d1f0df8ab9aeb971274e8b139c7b7eb082fc6b6b3320c6`; locator `company-link:https://www.instagram.com/granlystiftelse`; method `signalpost.website.v1`.

<pre>&lt;a href="https://www.instagram.com/granlystiftelse" &gt;</pre>

Source: https://www.granly-stiftelse.no/personvernerklaering/

Retrieved: 2026-11-17T17:33:55.462009Z; SHA-256 `14bd9ca90547097dbd93082d7a351e9be24f4bea7f9c4c25cd7a034dbb74d5f1`; locator `identity-proof:970351515`; method `signalpost.website.v1`.

<pre>r /&gt;
Telefon: 61 14 36 60&lt;br /&gt;
Org.nr: 970 351 515&lt;/p&gt;
&lt;p&gt;For spørsmål du måtte ha om vår behandling av dine personopplysninger kan du kontakte dagli</pre>

Source: https://www.granly-stiftelse.no/personvernerklaering/

Retrieved: 2026-11-17T17:33:55.462009Z; SHA-256 `14bd9ca90547097dbd93082d7a351e9be24f4bea7f9c4c25cd7a034dbb74d5f1`; locator `registry-contact:phone`; method `signalpost.registry_contact.v1`.

<pre>&lt;a style="color: #000000;" href="tel:+4761143660"&gt;</pre>

Source: https://www.granly-stiftelse.no/personvernerklaering/

Retrieved: 2026-11-17T17:33:55.462009Z; SHA-256 `14bd9ca90547097dbd93082d7a351e9be24f4bea7f9c4c25cd7a034dbb74d5f1`; locator `registry-contact:email_domain`; method `signalpost.registry_contact.v1`.

<pre>&lt;a style="color: #000000;" href="mailto:granly@granly-stiftelse.no"&gt;</pre>

### 975339688 - DIGERNES AS - social

- url: `https://www.linkedin.com/company/digernes-as`
- proof tier: `own_header_footer_exact_name_v1`
- automated verdict: **correct**

Source: https://www.digernes.no/

Retrieved: 2026-11-17T17:35:53.116691Z; SHA-256 `98dcc5a7f6ca9bc8f41fd6bfb8722bbff749702e24f22246b5cfc01c463eb035`; locator `company-link:https://www.linkedin.com/company/digernes-as`; method `signalpost.website.v1`.

<pre>&lt;a href="https://www.linkedin.com/company/digernes-as/" target="_blank"&gt;</pre>

Source: https://www.digernes.no/om-oss/pernsonvernerklaering

Retrieved: 2026-11-17T17:35:56.364412Z; SHA-256 `d8094de54dff4412a40717eaf65997b14a64c5e900e2cfd4c42bbf961c58d888`; locator `identity-proof:975339688`; method `signalpost.website.v1`.

<pre>ingsansvar&lt;/h3&gt;
&lt;p&gt;Digernes AS (Org.nr: 975 339 688) er behandlingsansvarlig for personopplysningene vi samler inn og behandler. Dette innebærer at vi</pre>

Source: https://www.digernes.no/om-oss/pernsonvernerklaering

Retrieved: 2026-11-17T17:35:56.364412Z; SHA-256 `d8094de54dff4412a40717eaf65997b14a64c5e900e2cfd4c42bbf961c58d888`; locator `registry-contact:phone`; method `signalpost.registry_contact.v1`.

<pre>&lt;a href="tel:4751779898"&gt;</pre>

### 985256055 - FRAMEWORKS AS - social

- url: `https://no.linkedin.com/company/frameworks-as`
- proof tier: `own_header_footer_exact_name_v1`
- automated verdict: **correct**

Source: https://frameworks.no/

Retrieved: 2026-11-17T17:35:33.256098Z; SHA-256 `09a6f3b7ec8bab0877adfa3b7d56e15bd2693b782ec14d9e8ccabeb9d90d4cfe`; locator `company-link:https://no.linkedin.com/company/frameworks-as`; method `signalpost.website.v1`.

<pre>&lt;a href="https://no.linkedin.com/company/frameworks-as" target="_blank" class="e-paragraph-link-base e-default-a"&gt;</pre>

Source: https://frameworks.no/

Retrieved: 2026-11-17T17:35:33.256098Z; SHA-256 `09a6f3b7ec8bab0877adfa3b7d56e15bd2693b782ec14d9e8ccabeb9d90d4cfe`; locator `identity-proof:985256055`; method `signalpost.website.v1`.

<pre>den 2012. Organisasjonsnummeret vårt er 985 256 055. Du når oss på telefon &lt;a href="tel:+4740400088"&gt;40 40 00 88&lt;/a&gt; eller på &lt;a href="mailto:simen.wi</pre>

Source: https://frameworks.no/

Retrieved: 2026-11-17T17:35:33.256098Z; SHA-256 `09a6f3b7ec8bab0877adfa3b7d56e15bd2693b782ec14d9e8ccabeb9d90d4cfe`; locator `registry-contact:email_domain`; method `signalpost.registry_contact.v1`.

<pre>&lt;a href="mailto:sw@frameworks.no" target="_self" class="e-paragraph-link-base e-default-a"&gt;</pre>

### 985256055 - FRAMEWORKS AS - social

- url: `https://twitter.com/Frameworks_AS`
- proof tier: `own_header_footer_exact_name_v1`
- automated verdict: **correct**

Source: https://frameworks.no/

Retrieved: 2026-11-17T17:35:33.256098Z; SHA-256 `09a6f3b7ec8bab0877adfa3b7d56e15bd2693b782ec14d9e8ccabeb9d90d4cfe`; locator `company-link:https://twitter.com/Frameworks_AS`; method `signalpost.website.v1`.

<pre>&lt;a href="https://twitter.com/Frameworks_AS" target="_blank" class="e-paragraph-link-base e-default-a"&gt;</pre>

Source: https://frameworks.no/

Retrieved: 2026-11-17T17:35:33.256098Z; SHA-256 `09a6f3b7ec8bab0877adfa3b7d56e15bd2693b782ec14d9e8ccabeb9d90d4cfe`; locator `identity-proof:985256055`; method `signalpost.website.v1`.

<pre>den 2012. Organisasjonsnummeret vårt er 985 256 055. Du når oss på telefon &lt;a href="tel:+4740400088"&gt;40 40 00 88&lt;/a&gt; eller på &lt;a href="mailto:simen.wi</pre>

Source: https://frameworks.no/

Retrieved: 2026-11-17T17:35:33.256098Z; SHA-256 `09a6f3b7ec8bab0877adfa3b7d56e15bd2693b782ec14d9e8ccabeb9d90d4cfe`; locator `registry-contact:email_domain`; method `signalpost.registry_contact.v1`.

<pre>&lt;a href="mailto:sw@frameworks.no" target="_self" class="e-paragraph-link-base e-default-a"&gt;</pre>

### 987693444 - ET BYGG AS - social

- url: `https://www.facebook.com/etbygg`
- proof tier: `own_header_footer_exact_name_v1`
- automated verdict: **correct**

Source: https://etbygg.com/

Retrieved: 2026-11-17T17:33:52.591267Z; SHA-256 `39840b221fae64efea13dfd02ba688fd6a81158f89e66b148c327d77df925c74`; locator `company-link:https://www.facebook.com/etbygg`; method `signalpost.website.v1`.

<pre>&lt;a href="https://www.facebook.com/etbygg" target="_blank" rel="noopener"&gt;</pre>

Source: https://etbygg.com/

Retrieved: 2026-11-17T17:33:52.591267Z; SHA-256 `39840b221fae64efea13dfd02ba688fd6a81158f89e66b148c327d77df925c74`; locator `identity-proof:987693444`; method `signalpost.website.v1`.

<pre>&gt; ET Bygg AS&lt;/span&gt;
      &lt;span&gt;Org.nr. 987 693 444&lt;/span&gt;
      &lt;span&gt;Medlem av Mesterhus&lt;/span&gt;
      &lt;!-- Vilkaarslenkene skyves bort fra selskapso</pre>

### 994479865 - IDENTUM AS - social

- url: `https://www.linkedin.com/company/identum-as`
- proof tier: `own_header_footer_exact_name_v1`
- automated verdict: **correct**

Source: https://www.identum.no/

Retrieved: 2026-11-17T17:32:01.564168Z; SHA-256 `356223741f48deba792eff2c569e1b2a0b4bdee0c59d567e77912eb72e1301d0`; locator `company-link:https://www.linkedin.com/company/identum-as`; method `signalpost.website.v1`.

<pre>&lt;a class="default-link nav-list__link " href="https://www.linkedin.com/company/identum-as/" target="_blank"&gt;</pre>

Source: https://www.identum.no/

Retrieved: 2026-11-17T17:32:01.564168Z; SHA-256 `356223741f48deba792eff2c569e1b2a0b4bdee0c59d567e77912eb72e1301d0`; locator `identity-proof:994479865`; method `signalpost.website.v1`.

<pre>"&gt;Organisasjonsnummer&lt;/h3&gt;
        &lt;p&gt;NO994479865 MVA&lt;/p&gt;
      &lt;/li&gt;
    
    &lt;/ul&gt;
  
&lt;/div&gt;
&lt;/div&gt;
        
      &lt;/div&gt;
      &lt;div class="footer-i</pre>

### 994479865 - IDENTUM AS - social

- url: `https://www.youtube.com/@identumAS`
- proof tier: `own_header_footer_exact_name_v1`
- automated verdict: **correct**

Source: https://www.identum.no/

Retrieved: 2026-11-17T17:32:01.564168Z; SHA-256 `356223741f48deba792eff2c569e1b2a0b4bdee0c59d567e77912eb72e1301d0`; locator `company-link:https://www.youtube.com/@identumAS`; method `signalpost.website.v1`.

<pre>&lt;a class="default-link nav-list__link " href="https://www.youtube.com/@identumAS" target="_blank"&gt;</pre>

Source: https://www.identum.no/

Retrieved: 2026-11-17T17:32:01.564168Z; SHA-256 `356223741f48deba792eff2c569e1b2a0b4bdee0c59d567e77912eb72e1301d0`; locator `identity-proof:994479865`; method `signalpost.website.v1`.

<pre>"&gt;Organisasjonsnummer&lt;/h3&gt;
        &lt;p&gt;NO994479865 MVA&lt;/p&gt;
      &lt;/li&gt;
    
    &lt;/ul&gt;
  
&lt;/div&gt;
&lt;/div&gt;
        
      &lt;/div&gt;
      &lt;div class="footer-i</pre>
