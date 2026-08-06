const PAGE_SIZE = 100;
let data = ROUND_1_DATA;
const DATA_BY_ROUND = { "Round 1": ROUND_1_DATA, "Round 2": ROUND_2_DATA, "Round 3": ROUND_3_DATA };
let currentRound = "Round 1";

const filterState = {
  quota: "",
  course: "",
  allottedCategory: "",
  candidateCategory: "",
  institute: "",
};

const COLUMN_META = {
  // sno: { label: "SNo", numeric: true }, // SNo column removed from UI; data still contains the field.
  rank: { label: "Rank", numeric: true },
  score: { label: "Score", numeric: true },
  quota: { label: "Allotted Quota", numeric: false },
  institute: { label: "Allotted Institute", numeric: false },
  course: { label: "Course", numeric: false },
  allottedCategory: { label: "Allotted Category", numeric: false },
  candidateCategory: { label: "Candidate Category", numeric: false },
  remarks: { label: "Remarks", numeric: false },
};

const FILTER_FIELDS = [
  { key: "quota", label: "Allotted Quota" },
  { key: "course", label: "Course" },
  { key: "allottedCategory", label: "Allotted Category" },
  { key: "candidateCategory", label: "Candidate Category" },
];

let sortKey = "rank";
let sortDir = "asc";
let page = 1;
let filteredRows = data.slice();

const fmt = (n) => n.toLocaleString("en-IN");

function uniqueSorted(key) {
  const set = new Set();
  for (const row of data) set.add(row[key]);
  return Array.from(set).sort((a, b) => a.localeCompare(b, undefined, { sensitivity: "base" }));
}

/* ---------- Single-select dropdown component ---------- */

function createDropdown(container, { key, label }) {
  const values = uniqueSorted(key);

  const root = document.createElement("div");
  root.className = "dropdown";

  root.innerHTML = `
    <label>${label}</label>
    <button type="button" class="dropdown-trigger">
      <span class="dd-label is-muted">All</span>
      <span class="dd-arrow">&#9662;</span>
    </button>
    <div class="dropdown-panel">
      <input type="text" class="dd-search" placeholder="Search ${label}…" autocomplete="off">
      <div class="dd-options"></div>
    </div>
  `;

  const trigger = root.querySelector(".dropdown-trigger");
  const panel = root.querySelector(".dropdown-panel");
  const search = root.querySelector(".dd-search");
  const optionsBox = root.querySelector(".dd-options");
  const labelEl = root.querySelector(".dd-label");

  function renderOptions(query = "") {
    optionsBox.innerHTML = "";
    const q = query.trim().toLowerCase();

    const anyBtn = document.createElement("button");
    anyBtn.type = "button";
    anyBtn.className = "dd-option dd-any" + (filterState[key] === "" ? " selected" : "");
    anyBtn.textContent = "All";
    anyBtn.addEventListener("click", () => {
      filterState[key] = "";
      labelEl.textContent = "All";
      labelEl.classList.add("is-muted");
      close();
      renderOptions();
    });
    optionsBox.appendChild(anyBtn);

    let shown = 0;
    for (const value of values) {
      if (q && !value.toLowerCase().includes(q)) continue;
      const opt = document.createElement("button");
      opt.type = "button";
      opt.className = "dd-option" + (filterState[key] === value ? " selected" : "");
      opt.textContent = value;
      opt.title = value;
      opt.addEventListener("click", () => {
        filterState[key] = value;
        labelEl.textContent = value;
        labelEl.classList.remove("is-muted");
        close();
        renderOptions();
      });
      optionsBox.appendChild(opt);
      shown++;
    }

    if (shown === 0) {
      const empty = document.createElement("div");
      empty.className = "dd-empty";
      empty.textContent = "No matches";
      optionsBox.appendChild(empty);
    }
  }

  function open() {
    root.classList.add("open");
    renderOptions();
    search.value = "";
    search.focus();
  }

  function close() {
    root.classList.remove("open");
  }

  trigger.addEventListener("click", (e) => {
    e.stopPropagation();
    root.classList.contains("open") ? close() : open();
  });

  search.addEventListener("input", () => renderOptions(search.value));
  search.addEventListener("keydown", (e) => {
    if (e.key === "Escape") close();
  });

  document.addEventListener("click", (e) => {
    if (!root.contains(e.target)) close();
  });

  container.appendChild(root);
}

/* ---------- Institute autocomplete ---------- */

function createInstituteAutocomplete(container) {
  const institutes = uniqueSorted("institute");

  const root = document.createElement("div");
  root.className = "autocomplete";
  root.innerHTML = `
    <input type="text" placeholder="Search Allotted Institute…" autocomplete="off">
    <button type="button" class="ac-clear" title="Clear institute">&times;</button>
    <div class="ac-list"></div>
  `;

  const input = root.querySelector("input");
  const clear = root.querySelector(".ac-clear");
  const list = root.querySelector(".ac-list");

  function updateClear() {
    clear.classList.toggle("visible", filterState.institute !== "");
  }

  function renderMatches(query) {
    list.innerHTML = "";
    const q = query.trim().toLowerCase();

    if (filterState.institute && query.trim() === filterState.institute) {
      showResult(filterState.institute);
      return;
    }

    if (!q) {
      list.classList.remove("visible");
      return;
    }

    const matches = institutes.filter((inst) => inst.toLowerCase().includes(q)).slice(0, 50);

    if (matches.length === 0) {
      const empty = document.createElement("div");
      empty.className = "ac-empty";
      empty.textContent = "No matching institutes";
      list.appendChild(empty);
    } else {
      for (const inst of matches) {
        const item = document.createElement("button");
        item.type = "button";
        item.className = "ac-item";
        item.textContent = inst;
        item.title = inst;
        item.addEventListener("click", () => {
          select(inst);
        });
        list.appendChild(item);
      }
    }
    list.classList.add("visible");
  }

  function select(inst) {
    filterState.institute = inst;
    input.value = inst;
    list.classList.remove("visible");
    updateClear();
  }

  function showResult(inst) {
    list.innerHTML = "";
    const item = document.createElement("button");
    item.type = "button";
    item.className = "ac-item";
    item.textContent = inst;
    item.title = inst;
    item.addEventListener("click", () => select(inst));
    list.appendChild(item);
    list.classList.add("visible");
  }

  input.addEventListener("input", () => {
    if (filterState.institute && input.value !== filterState.institute) {
      filterState.institute = "";
    }
    updateClear();
    renderMatches(input.value);
  });

  input.addEventListener("focus", () => {
    if (input.value.trim()) renderMatches(input.value);
  });

  input.addEventListener("keydown", (e) => {
    if (e.key === "Escape") list.classList.remove("visible");
  });

  document.addEventListener("click", (e) => {
    if (!root.contains(e.target)) list.classList.remove("visible");
  });

  clear.addEventListener("click", () => {
    filterState.institute = "";
    input.value = "";
    list.classList.remove("visible");
    updateClear();
  });

  const wrap = document.createElement("div");
  wrap.className = "filter-control filter-institute";
  const lbl = document.createElement("label");
  lbl.textContent = "Allotted Institute";
  wrap.appendChild(lbl);
  wrap.appendChild(root);
  container.appendChild(wrap);
  updateClear();
}

/* ---------- Filtering / sorting / pagination ---------- */

function applyFilters() {
  page = 1;
  filteredRows = data.filter((row) => {
    if (filterState.quota && row.quota !== filterState.quota) return false;
    if (filterState.course && row.course !== filterState.course) return false;
    if (filterState.allottedCategory && row.allottedCategory !== filterState.allottedCategory) return false;
    if (filterState.candidateCategory && row.candidateCategory !== filterState.candidateCategory) return false;
    if (filterState.institute && row.institute !== filterState.institute) return false;
    return true;
  });
  sortRows();
  render();
}

function sortRows() {
  const meta = COLUMN_META[sortKey];
  const dir = sortDir === "asc" ? 1 : -1;
  filteredRows.sort((a, b) => {
    if (meta.numeric) {
      return (Number(a[sortKey]) - Number(b[sortKey])) * dir;
    }
    return a[sortKey].localeCompare(b[sortKey], undefined, { sensitivity: "base" }) * dir;
  });
}

function render() {
  const total = filteredRows.length;
  const totalPages = Math.max(1, Math.ceil(total / PAGE_SIZE));
  page = Math.min(page, totalPages);

  const start = (page - 1) * PAGE_SIZE;
  const slice = filteredRows.slice(start, start + PAGE_SIZE);

  const body = document.getElementById("table-body");
  body.innerHTML = "";

  if (slice.length === 0) {
    const tr = document.createElement("tr");
    tr.innerHTML = '<td colspan="8" class="empty-cell">No rows match your current filters.</td>';
    body.appendChild(tr);
  } else {
    for (const row of slice) {
      const tr = document.createElement("tr");
      // "sno" intentionally omitted — SNo column removed from UI.
      for (const key of ["rank", "score", "quota", "institute", "course", "allottedCategory", "candidateCategory", "remarks"]) {
        const td = document.createElement("td");
        td.textContent = row[key];
        if (key === "rank") td.className = "col-rank";
        if (key === "score") td.className = "col-score";
        if (key === "institute" || key === "course") td.title = row[key];
        tr.appendChild(td);
      }
      body.appendChild(tr);
    }
  }

  const end = total === 0 ? 0 : Math.min(start + slice.length, total);
  const countEl = document.getElementById("result-count");
  if (total === 0) {
    countEl.innerHTML = "<strong>0</strong> rows match your filters.";
  } else {
    countEl.innerHTML = `Showing <strong>${fmt(start + 1)}–${fmt(end)}</strong> of <strong>${fmt(total)}</strong> rows.`;
  }

  document.getElementById("prev-btn").disabled = page <= 1;
  document.getElementById("next-btn").disabled = page >= totalPages;
  document.getElementById("page-info").textContent = `Page ${fmt(page)} of ${fmt(totalPages)}`;
}

function clearAll() {
  for (const key of Object.keys(filterState)) filterState[key] = "";
  document.querySelectorAll(".dropdown .dd-label").forEach((el) => {
    el.textContent = "All";
    el.classList.add("is-muted");
  });
  const instInput = document.querySelector("#filter-institute input");
  if (instInput) {
    instInput.value = "";
    document.querySelector(".ac-clear").classList.remove("visible");
  }
  applyFilters();
}

/* ---------- Wire up ---------- */

function buildFilters() {
  document.getElementById("filter-quota").innerHTML = "";
  document.getElementById("filter-course").innerHTML = "";
  document.getElementById("filter-allotted").innerHTML = "";
  document.getElementById("filter-candidate").innerHTML = "";
  document.getElementById("filter-institute").innerHTML = "";

  for (const field of FILTER_FIELDS) {
    const container = document.getElementById("filter-" + {
      quota: "quota",
      course: "course",
      allottedCategory: "allotted",
      candidateCategory: "candidate",
    }[field.key]);
    createDropdown(container, field);
  }

  createInstituteAutocomplete(document.getElementById("filter-institute"));
}

function switchRound(round) {
  if (round === currentRound) return;
  currentRound = round;
  data = DATA_BY_ROUND[round];
  for (const key of Object.keys(filterState)) filterState[key] = "";
  page = 1;
  sortKey = "rank";
  sortDir = "asc";
  buildFilters();
  applyFilters();
}

function init() {
  buildFilters();

  document.getElementById("apply-btn").addEventListener("click", applyFilters);
  document.getElementById("clear-btn").addEventListener("click", clearAll);
  document.querySelectorAll('input[name="round"]').forEach((radio) => {
    radio.addEventListener("change", () => switchRound(radio.value));
  });
  document.getElementById("prev-btn").addEventListener("click", () => {
    page = Math.max(1, page - 1);
    render();
  });
  document.getElementById("next-btn").addEventListener("click", () => {
    page += 1;
    render();
  });

  document.querySelectorAll("thead th").forEach((th) => {
    th.addEventListener("click", () => {
      const key = th.dataset.key;
      if (sortKey === key) {
        sortDir = sortDir === "asc" ? "desc" : "asc";
      } else {
        sortKey = key;
        sortDir = "asc";
      }
      sortRows();
      render();
    });
  });

  applyFilters();
}

init();
