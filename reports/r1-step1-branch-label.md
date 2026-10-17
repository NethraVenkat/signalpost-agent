# R1 Step 1 — registered-subunit website relationship label

17 October 2026. Branch `revision/r1`, based on submitted `3944c89`.
Step 1 only. Local commit; not pushed or tagged. Final revision gates remain pending.

## Change

When an `official_website` claim is proven by the exact registered subunit
number, its existing `reasons` map now contains:

```json
{"relationship": "Website of registered subunit 933248380"}
```

The existing `value.matched_via_subunit`, value, claim ID, evidence IDs and
registered parent/subunit evidence remain unchanged. Parent/group metadata is
preserved. A candidate nominated by a subunit but proven by the main company's
number is not mislabelled as a branch match.

The site displays the explicit label next to the website fact. Rendering derives
the text from `matched_via_subunit`, so saved pre-revision branch claims also
display correctly without rewriting their facts or evidence.

No discovery, identity matching, robots, budget, source selection or output-schema
change. No facts added or removed. The existing Claim.reasons field is used to
avoid changing canonical values and therefore claim IDs.

## Verification

- Focused branch, site, identity-scope and external replay checks: **34 passed**.
- Full suite: **465 passed in 92.02 seconds**.
- New tests exercise actual website publication with exact subunit proof and
  exact parent proof, preserve the canonical claim ID and registered-branch
  evidence, validate the Claim schema, and verify both new and historical HTML.
- Saved FILMTEK AS (`988330752`) / audioped.no / registered subunit `933248380`
  regenerated successfully: the explicit relationship label is present in
  `out/r1-step1/site/c/988330752.html`; profile HTML is 78,907 bytes.
- Browser viewport checks were not repeated for this text-only change. No live
  1,000-company crawl, final idempotency gate, final CI, clean-clone smoke, or
  release tag is claimed at this checkpoint.

Stopped after Step 1. Steps 2–6 have not been started by this change.
