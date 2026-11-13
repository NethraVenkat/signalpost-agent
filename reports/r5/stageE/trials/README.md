# Offline harness development trials

These superseded trials are not the final measurement. No production code changed. The first trial exposed a harness expected-field typo for the business-address mutation and an invalid offline NAV token shape. The next corrected the expectation and token but exposed that forward feed bodies were never persisted. The third explicitly supplied an empty completed forward tail, detected all seven interventions and had zero unexpected events. The final fixture also pins a one-ad NAV index, eliminating dependency on the changing bundled index; final results are ../refresh_results.json and verified by the CI tests.

No live feed coverage claim is made from the scaffold. Source bodies used for claims remain exact saved receipts. Initial direct-script import failure is a harness setup failure, not an application/refresh result.
