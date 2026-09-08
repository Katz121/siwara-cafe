# English attribute translation fix

## Root cause

`translate_attrs()` used a regex ending in the control character `\x02`, rather than the intended backreference `\2`. The pattern therefore never matched quoted attributes. After fixing the matcher, the replacement now emits exactly one closing quote.

## Changes

- Fixed the closing-quote backreference in `build_en.py`.
- Fixed attribute replacement so translated values do not create doubled quotes.
- Added `test_translate_attrs.py` covering translated, missing, and non-Thai values.

## Verification

- `python -m unittest -v test_translate_attrs.py`: 3 tests passed.
- `python build_en.py`: 44 English pages generated; 0 skipped.
- `placeholder="พิมพ์...` in `site/en/eat/index.html`: 0 matches.
- Nested doubled attribute quotes in `site/en`: 0 matches.

## Remaining attribute audit

The post-build scan found Thai values in `alt`, `title`, and `aria-label` attributes outside the reported placeholder. These are untranslated source/UI strings (for example the shared navigation and theme labels), not matcher failures; they are recorded by the existing missing-translation report for follow-up translation entries.
