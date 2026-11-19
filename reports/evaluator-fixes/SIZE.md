# Generated-data cleanup

| Measurement | Bytes |
|---|---:|
| Tracked working-file contents before cleanup | 1,610,661,415 |
| Removed generated JSON | 1,176,953,493 |
| Remaining tracked contents before adding new fix receipts | 433,707,922 |

Removed 211 uncited generated JSON files. The [complete manifest](PRUNED_DATA.json) records paths, sizes, original Git blob IDs and the citation checks used. All Markdown, cohort CSV/JSONL inputs, source bodies, screenshots, human-review records, licence declarations and explicitly cited receipts were retained. No deleted file is a target of a retained Markdown link.

The original public clone took 80.05 seconds and contained about 1.78 GB of file contents including Git. That network time is a historical measurement, not a prediction for the revised commit. Git history was preserved: ordinary full-history clones can still download old objects. A fresh shallow checkout of the revised tip excludes these generated files; its measured size is recorded after the evidence commit.
