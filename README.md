# NEET PG Allotment Viewer

A fast, browser-based viewer for the **NEET PG 2025** (MCC All India Counseling, Round 1) seat allotment results. Load the entire allotment dataset and filter, search, and sort your way through 26,889 allotments — no server required.

Built with plain HTML, CSS, and JavaScript. No frameworks, no dependencies, no build step.

## Live site

👉 [https://crockzo.github.io/neet-pg/](https://crockzo.github.io/neet-pg/)

## What it does

- **View** all 26,889 allotment rows (2025, MCC All India Counseling Round 1) in a paginated table (100 rows per page).
- **Filter** by four columns simultaneously:
  - Allotted Quota
  - Course
  - Allotted Category
  - Candidate Category
- **Search** for a specific Allotted Institute with an autocomplete dropdown (works in combination with all other filters).
- **Sort** any column — click a column header to toggle ascending/descending (e.g. by Rank for cutoff analysis).
- **Reset** everything with a single **Clear All** button.
- See a live row count of how many allotments match your current filters.

Filters are applied only when you click **Apply Filter**, so you can build up a combination before seeing results.

## Project structure

| File             | Purpose                                                              |
| ---------------- | -------------------------------------------------------------------- |
| `index.html`     | Page markup                                                          |
| `styles.css`     | Light theme styling                                                  |
| `script.js`      | Filtering, autocomplete, sorting, and pagination logic               |
| `data.js`        | The allotment data as a bundled JS file (generated, ~7.8 MB)         |
| `convert_xlsx.py`| Rebuilds `data.js` from `neet-pg-document.xlsx` (Python stdlib only) |
| `.nojekyll`      | Tells GitHub Pages to serve the files as-is                          |

## Running locally

Just open `index.html` in your browser:

```bash
open index.html
```

No local server needed — the data is bundled into `data.js` and everything works from `file://`.

## Regenerating the data

If you have an updated copy of the spreadsheet named `neet-pg-document.xlsx` in this directory:

```bash
python3 convert_xlsx.py
```

This rewrites `data.js` from the spreadsheet. Requires Python 3 with no extra packages.

## Data source & credits

The allotment data is from the **NEET PG 2025** results — specifically **MCC All India Counseling, Round 1**. It was obtained from the following Reddit post in r/indianmedschool:

- [MCC All India Counseling Round 1 2025 Excel](https://www.reddit.com/r/indianmedschool/comments/1p2zhoa/mcc_all_india_counseling_round_1_2025_excel/)

> **Note:** This is an unofficial, community-shared copy of the data, provided for reference only. Always verify the latest information against the official [Medical Counselling Committee (MCC)](https://mcc.nic.in/) website.

## Disclaimer

This project is not affiliated with or endorsed by the Medical Counselling Committee (MCC), the National Medical Commission (NMC), or Reddit. It is a personal tool for exploring publicly shared allotment data.

## License

This project is for personal/educational use. The underlying allotment data belongs to the respective authorities.
