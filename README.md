# Asiana Gold — website source

The website of Asiana Gold, an 18K gold chain factory in Ho Chi Minh City,
running at <https://www.asiana-gold.com>.

The site is **a single static HTML file**. `shell.html` holds the entire page —
markup, styles, router and rendering — and the catalogue is injected at build
time. No application server, no compile step, no external dependencies.

## What this repository deliberately leaves out

This repository is public, so the company's data stays out of it:

| Not here | Why |
|---|---|
| `payload.json`, `products_full.json`, `specs.json`, `avail.json` | the catalogue, weight tables, availability and MOQ |
| `img/` — 456 product photographs | studio photography is company property |
| The two `KS011A` / `KS011B ... .xlsx` workbooks | the source of everything above |
| The built `index.html` | it carries the whole catalogue inlined |

`.gitignore` blocks all of them. **Do not remove those lines.**

Rebuilding the site therefore needs the two source spreadsheets, which are not
distributed here.

## Layout

```
shell.html          the whole page: HTML + CSS + JS, with a slot for the data
assemble.py         shell.html + payload.json -> index.html
vercel.json         hosting: SPA routing, caching, apex redirect
build_full.py       lifts products and photographs out of the workbooks
build_specs2.py     lifts the specification and availability tables
merge_full.py       folds everything into payload.json
keyout.py           keys the white studio background out of a chain shot
make_hero_cbyw.py   builds one hero cut-out from a supplied photograph
legacy/             one-shot edits already folded into shell.html
```

`shell.html` reads its content from exactly one place:

```js
const DATA = /*__PAYLOAD__*/{products:[],specs:[]};
```

`assemble.py` replaces the string `/*__PAYLOAD__*/{products:[],specs:[]}` with
the contents of `payload.json` and writes `index.html`. Opening `shell.html`
directly in a browser gives you a working but empty site — that is by design.

## Building

Needs Python 3 and Pillow:

```bash
pip install pillow
```

Put the two source workbooks side by side, then run in order:

```bash
python build_full.py <output-dir> "KS011A ... .xlsx" "KS011B ... .xlsx"
python build_specs2.py "KS011B ... .xlsx"
python merge_full.py <output-dir>
python assemble.py
```

This produces `payload.json`, an `img/` directory and `index.html`. All three
are ignored by git.

## Deploying

The site runs on Vercel, project `hpvn/asiana-gold-preview-site`.

```bash
vercel deploy --prod --yes
```

The deploy directory needs `index.html`, `img/` and `vercel.json`.

`vercel.json` does three things:

- **rewrites** — every path returns `index.html` so `/home`, `/catalogue` and
  `/product/CY25SR` work. `/img/` is excluded, so a missing image gives a real
  404 instead of HTML with a 200.
- **redirects** — `asiana-gold.com` sends a 308 to `www.asiana-gold.com`,
  keeping the path.
- **headers** — images cache for a year (filenames are content hashes, so a
  changed image is a changed name); HTML is never cached.

## Things that bite

**Image paths must be absolute, `/img/...`.** With `img/...`, a browser on
`/product/CY25SR` looks for `/product/img/...`, and because the catch-all
rewrite answers everything, it gets HTML back with a 200 — the image breaks
with no error anywhere.

**A photograph in the workbook belongs to the code directly beneath it, in its
own column.** Anything looser mixes up neighbouring variants. `build_full.py`
holds to that rule.

**A standalone HTML file must carry its own `<meta charset="utf-8">`.** Without
it every Vietnamese diacritic on the page breaks.
