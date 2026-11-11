# Academic portfolio: build sources

The academic pages (`academic.html` and everything in `academic/`) are generated. Edit the files here, then rebuild. Don't hand-edit the generated pages: the next build overwrites them.

## Rebuild

From the repository root:

```
python3 _build/academic/v5/compose.py
python3 _build/academic/build5.py
```

`compose.py` assembles the page bodies into `v5/out/`. `build5.py` wraps them with the head, styles and scripts from `index.html` and writes the pages, each with `noindex`.

## Regenerate the CV PDF

Serve the repository root on port 8791 (`python3 -m http.server 8791`), copy `v5/cv-print.html` to the root as `_cvprint.html`, run `node _build/academic/v5/pdf.js`, then delete `_cvprint.html`. This writes `academic/Muiz_Fuad_CV.pdf`: the light version on the #F4F6FA tint.

## Check

With the same server running, `node _build/academic/v5/check.js` loads every page on desktop and phone and reports script errors, broken links and sideways overflow.

## Where things live

- `body.v4.html`: the original one-page content, including the `acData` JSON (modules, evaluation scores, outcomes). `compose.py` corrects facts in it (the `FIX` list), then cuts it into pages.
- `v5/compose.py`: the page structure, module pages, CV document and Research talks.
- `v5/css2.css`: styles for the multi-page site, the CV, the back button and the activity dashboard.
- `extra.js`, `extra2.js`, `tw.js`: certificates and menu, charts and clips, the Teaching Wheel.
- `v5/header.html`, `v5/footer.html`, `v5/home_*.html`, `v5/activity_*`: shared fragments.

Only content that's already public on the site belongs here. Never add the handoff files, the scoring spec, `src/`, the Apps Script, marksheets or referee details.
