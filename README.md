# NEET PG Allotment Viewer

A fast, browser-based viewer for the **NEET PG 2025** (MCC All India Counseling, Round 1) seat allotment results. Load the entire allotment dataset and filter, search, and sort your way through ~66,000 allotments — no server required.

Built with plain HTML, CSS, and JavaScript. No frameworks, no dependencies, no build step.

## Live site

👉 [https://crockzo.github.io/neet-pg/](https://crockzo.github.io/neet-pg/)

## What it does

- **View** allotment rows for Round 1 (26,889), Round 2 (20,787) or Round 3 (18,673) — switch datasets with the round selector, 100 rows per page.
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
| `index.html`     | Page markup (incl. round selector)                                   |
| `styles.css`     | Light theme styling                                                  |
| `script.js`      | Round switching, filtering, autocomplete, sorting, pagination logic  |
| `round-1/data.js`| Round 1 allotment data as a bundled JS file (generated, ~8 MB)       |
| `round-2/data.js`| Round 2 allotment data as a bundled JS file (generated, ~6.5 MB)     |
| `round-3/data.js`| Round 3 allotment data as a bundled JS file (generated, ~6.4 MB)     |
| `.nojekyll`      | Tells GitHub Pages to serve the files as-is                          |

## Running locally

Just open `index.html` in your browser:

```bash
open index.html
```

No local server needed — the data is bundled into `data.js` and everything works from `file://`.

## Data source & credits

The allotment data is from the **NEET PG 2025** results — specifically **MCC All India Counseling, Round 1**. It was obtained from the following Reddit post in r/indianmedschool:

- [Inspired by this reddit post](https://www.reddit.com/r/indianmedschool/comments/1p2zhoa/mcc_all_india_counseling_round_1_2025_excel/)

- [Round 1 data source](https://cdnbbsr.s3waas.gov.in/s3e0f7a4d0ef9b84b83b693bbf3feb8e6e/uploads/2025/11/202511221303622410.pdf)

- [Round 2 data source](https://cdnbbsr.s3waas.gov.in/s3e0f7a4d0ef9b84b83b693bbf3feb8e6e/uploads/2025/12/202512172132273940.pdf)

- [Round 3 data source](https://cdnbbsr.s3waas.gov.in/s3e0f7a4d0ef9b84b83b693bbf3feb8e6e/uploads/2026/02/20260206892439077.pdf)

> **Note:** This is an unofficial, community-shared copy of the data, provided for reference only. Always verify the latest information against the official [Medical Counselling Committee (MCC)](https://mcc.nic.in/) website.

## Disclaimer

This project is not affiliated with or endorsed by the Medical Counselling Committee (MCC), the National Medical Commission (NMC), or Reddit. It is a personal tool for exploring publicly shared allotment data

## License

This project is for personal/educational use. The underlying allotment data belongs to the respective authorities.
