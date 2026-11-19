# Website deadline diagnosis

The earlier audit batch had 97 valid identifiers and three malformed records. All 42 deadline-affected companies lost website research. Pass 2 started at 250.859 seconds and stopped at 340.015 seconds; the fixed run budget was 2,100 seconds. These are unfinished proof checks, not a claim that 42 correct websites existed.

| Organisation number | Interrupted section | Recorded state |
|---|---|---|
| 925181536 | website | failed |
| 829577372 | website | failed |
| 932525070 | website | failed |
| 915188389 | website | ambiguous |
| 936035523 | website | failed |
| 936349676 | website | failed |
| 927439794 | website | failed |
| 918843183 | website | failed |
| 930621927 | website | failed |
| 956409071 | website | not_available |
| 912579433 | website | failed |
| 991835423 | website | ambiguous |
| 997995414 | website | available |
| 957687504 | website | failed |
| 916249985 | website | ambiguous |
| 814635562 | website | available |
| 918953612 | website | not_available |
| 950302011 | website | not_available |
| 928892956 | website | not_available |
| 928054780 | website | failed |
| 929676130 | website | not_available |
| 998320143 | website | failed |
| 927157985 | website | not_available |
| 928565637 | website | failed |
| 930777102 | website | failed |
| 932112183 | website | failed |
| 998795621 | website | failed |
| 960480120 | website | not_available |
| 993016446 | website | failed |
| 931515152 | website | not_available |
| 833467972 | website | not_available |
| 925590266 | website | failed |
| 983739377 | website | failed |
| 925841722 | website | failed |
| 998181410 | website | failed |
| 933581411 | website | failed |
| 917403562 | website | not_available |
| 931605712 | website | failed |
| 925622605 | website | failed |
| 934843355 | website | not_available |
| 998309530 | website | failed |
| 912702847 | website | failed |

## Fresh 100-valid-company check after fixes 1–2

The documented run took 674.97 seconds and recorded 96 deadline-affected companies. Its first pass exceeded the former 340-second cutoff.

| Organisation number | Interrupted sections |
|---|---|
| 925181536 | website |
| 829577372 | website |
| 932525070 | website |
| 919263601 | website |
| 988963259 | website |
| 915188389 | website |
| 934485718 | website |
| 936035523 | website |
| 936349676 | website |
| 935962196 | website |
| 997095987 | website |
| 950310499 | website |
| 948639416 | website |
| 927439794 | website |
| 975514412 | website |
| 918843183 | website |
| 934216385 | website |
| 935647142 | website |
| 930621927 | website |
| 946595845 | website |
| 956409071 | website |
| 912579433 | website |
| 918982523 | website |
| 991835423 | website |
| 919414944 | website |
| 918079327 | website |
| 923399658 | website |
| 933025160 | website |
| 997995414 | website |
| 957687504 | website |
| 916249985 | website |
| 814635562 | website |
| 927342677 | website |
| 918953612 | website |
| 820162692 | website |
| 950302011 | website |
| 912435911 | website |
| 999504116 | website |
| 928892956 | website |
| 927177978 | website |
| 929868323 | website |
| 935465567 | website |
| 928054780 | website |
| 934962435 | website |
| 929676130 | website |
| 998320143 | website |
| 918109099 | website |
| 922688532 | website |
| 926489380 | website |
| 927157985 | website |
| 928565637 | website |
| 930777102 | website |
| 932112183 | website |
| 926201905 | website |
| 929141369 | website |
| 899174682 | website |
| 916374801 | website |
| 998795621 | website |
| 918703853 | website |
| 960480120 | website |
| 993016446 | website |
| 928542742 | website |
| 931515152 | website |
| 929603176 | website |
| 833467972 | website |
| 925590266 | website |
| 983739377 | website |
| 925841722 | website |
| 926433873 | website |
| 917751412 | website |
| 926358154 | website |
| 932004437 | website |
| 998181410 | website |
| 989214209 | website |
| 933581411 | website |
| 912238504 | website |
| 917403562 | website |
| 989965964 | website |
| 931605712 | website |
| 815566602 | website |
| 925622605 | website |
| 934843355 | website |
| 998309530 | website |
| 934836189 | website |
| 928597695 | website |
| 915596436 | website |
| 912702847 | website |
| 998340888 | website |
| 915412262 | website |
| 930012130 | website |
| 918824642 | website |
| 928027678 | website |
| 913129601 | website |
| 987769386 | website |
| 934616081 | website |
| 917281696 | website |

## Correction

The website-only window now uses the fixed budget rather than multiplying it by N/500. At both 100 and 500 inputs it ends at 1,700 seconds, leaving the existing 400-second finalisation/margin reserve. The 2,100-second total, 1,785-second crawl deadline, per-company and global HTTP limits, robots checks and domain pacing are unchanged. Custom budgets and scaled opt-in behavior retain their original deadlines.

Nineteen targeted budget/reserve tests passed, including a proof request after 600 elapsed seconds that used to be rejected. A fresh live check follows the robots correction; remaining genuine safety-limit failures will stay visible.
