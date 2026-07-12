# Alex Strong's Compost Calculator

A single-page, offline-capable web app for designing multi-ingredient compost recipes. You tell it what feedstocks you have on hand and how much of each, rank what matters most (moisture, density, or C:N ratio), and it builds a phased "Operations Sheet" telling you exactly how much of each ingredient to load onto the pad.

**Live:** [alexstrong.design/tools/compost/](https://alexstrong.design/tools/compost/)

No install, no server, no internet connection required — works identically whether you open it from that link or just open the HTML file directly in a browser.

## Quick Start

1. Open the [live app](https://alexstrong.design/tools/compost/) or [`alexs-compost-calculator_v2.html`](alexs-compost-calculator_v2.html) directly in any modern browser (Chrome, Edge, Safari, Firefox).
2. Click **+ Start a New Recipe**.
3. Walk through the four tabs in order: **Constraints → Ingredients → Operations Sheet**.
4. Save the result to your Recipe Book so you can reload, print, or annotate it later.

Everything is saved locally in your browser (via `localStorage` and `IndexedDB`) — nothing is uploaded anywhere.

Opens in dark mode by default — click the 🌙/☀️ toggle in the top right to switch, and it remembers your choice.

### Deployment

This repo (`Alex-Strongs-Compost-Calculator`) is the source of truth. The live copy at `alexstrong.design/tools/compost/` is a manually-synced copy of [`alexs-compost-calculator_v2.html`](alexs-compost-calculator_v2.html) at `static/tools/compost/index.html` in the `Alex-G-Strong.github.io` (Hugo) repo. After making changes here, re-push the file there to update the live site.

## Walkthrough

### 1. Recipe Book
This is the home tab. It lists every recipe you've saved, showing the date, total volume, and final pile health metrics for each. From here you can:
- **Load Input** — pull a saved recipe back onto the workbench to tweak and re-solve it.
- **+ Note** — attach a dated field note (and optionally a photo) to a recipe, e.g. to log how the pile actually turned out.
- **Export** — download a single recipe as a `.json` file.
- **Export All** — back up your entire recipe book as one `.json` file.
- **Import** — load a `.json` file exported from this app (yours or someone else's). Useful for moving recipes between devices — see the FAQ tab for AirDrop/Nearby Share instructions.
- **🔗 Share** — generates a link and a scannable QR code that encode just that recipe's ingredients and settings (not your saved results, notes, or photos). Anyone who opens the link or scans the code — even on a device that's never used this app before — gets that recipe loaded straight into their own calculator, ready to solve and save. Nothing is uploaded anywhere; the entire recipe is encoded directly in the URL itself.
- **✕** — delete a recipe.

A status line under the header shows whether an automatic backup file is linked (see [Automatic File Backup](#automatic-file-backup-chrome-edge-opera) below) — or, on non-Chromium browsers, a note that automatic backup isn't available there.

Click **+ Start a New Recipe** to clear the workbench and begin.

### 2. Constraints — Site & Batch Settings
Set up the batch before adding ingredients:

- **Measurement Unit** — the physical unit you'll actually use on the pad: Cubic Yards, Cubic Meters, a custom loader bucket size, Wheelbarrow (~6 cu ft), or 5-Gallon Bucket. All ingredient quantities and results will be shown in this unit.
  - Selecting **Cubic Meters** switches the whole batch-sizing workflow to metric: the Target Batch Volume field and the Pile Dimensions fields (Length/Width/Height) switch from cuyd/ft to m³/meters, and the calculated/solved volumes are reported back in m³. Any other unit choice keeps dimensions in feet and volumes in cubic yards. (Ingredient chemistry values — C:N, density, moisture, structural index — stay in their original units regardless of the measurement unit chosen.)
- **Define Batch Size By** — either:
  - **Direct Volume**: enter a target volume (cubic yards, or cubic meters if that unit is selected), or
  - **Pile Dimensions**: enter Length × Base Width × Height (in feet, or meters if Cubic Meters is selected), and the tool calculates volume using a parabolic pile profile (`Base × Height × 0.67 × Length`). If your height exceeds 5/8 of the base width, it warns you the pile risks over-compaction and will need a high structural index.

**Optimization Priorities & Ranges** — drag the three cards (using the `≡` handle) into the order that matters most to you:
- **Moisture (%)** — target 55–65%. Too dry slows decomposition; too wet goes anaerobic and smells.
- **Density (lb/yd³ or kg/m³)** — target 600–800 lb/yd³ (≈356–475 kg/m³ if Cubic Meters is selected). A proxy for porosity/airflow.
- **C:N Ratio** — target 25–35. The carbon ("browns") to nitrogen ("greens") balance that feeds the microbes.

You can edit the min/max range for each metric. **The solver strictly prioritizes whichever card is on top** — if your feedstocks can't satisfy all three ranges at once, it sacrifices the lowest-ranked one first.

Click **Next: Add Ingredients →** when ready.

### 3. Ingredients
Build your list of available feedstocks. For each row:

- **Ingredient Name** — start typing to autocomplete from the built-in library (Horse Manure, Wood Chips, Grass Clippings, Cow Manure, Poultry Manure, Vegetable Scraps, Coffee Grounds, Dry Leaves, Straw, Cardboard/Paper, Sawdust, Food Waste) or your own saved custom items. Picking a known name auto-fills the fields below. This autocomplete is intentionally limited to that short list plus your own items — it does **not** search the large reference database below (use the Ingredient Library modal for that).
- **C:N** — carbon-to-nitrogen ratio.
- **Density** — bulk weight in lb/yd³ (or kg/m³ if Cubic Meters is the active unit).
- **Moist.** — moisture percentage.
- **Struct.** (Structural Index, 1–10) — resistance to compaction. 10 = rigid (wood chips), 1 = mushy (food waste). See the FAQ tab for why this matters.
- **Avail. Inventory** — the maximum amount you actually have on hand, in whatever unit you chose in Constraints. Leave blank for unlimited. **The solver will never exceed this limit.**

For a feedstock not in the library, fill in the values yourself (lab test results, a web search, or a reasonable estimate) and click **Save to Lib** to reuse it in future recipes.

**📚 Ingredient Library** (button at the top of this tab) opens a much larger reference tool:
- **Your Items** — your own saved custom ingredients (editable in place, with Save/Load/Delete).
- **Reference Database** — 134 real, named feedstocks (manures, yard trimmings, wood & paper, food waste, crop residues, straw/hay/silage, meat/fish by-products, liquids) pulled from [`dev/categorized_compost_database.csv`](dev/categorized_compost_database.csv), grouped into collapsible categories with C:N, Density, Moisture, and SI shown for each.
- A **search bar** filters both sections live by name and auto-expands any category with a match.
- Each row has an optional **Inventory** field and a **Load** button — set an amount (or leave blank for unlimited) and click Load to drop that ingredient straight into a new row on your Ingredients tab.

Click **+ Add Row** to add more feedstocks (you need at least 2), then **Generate Phased Operations Sheet →** to run the solver.

### 4. Operations Sheet (Results)
This tab shows what the solver came up with:

- **Status banner** — green if the full target volume was built within your health ranges; red if it halted early (ran out of inventory, or couldn't add more material without breaking the chemistry targets).
- **Total Pile Yield** — total volume (in your chosen unit) and weight (tons).
- **Overall Pile Health** — moisture, density, and C:N ratio, color-coded green/red against your target ranges, plus a Structure Score (target 5.0+).
- **Total Recipe Summary** — how much of each ingredient to use in total, flagged if that ingredient got fully used up ("Exhausted").
- **Phase Construction Breakdown** — the pile is built in sequential *phases*. Each phase is a fixed ratio of ingredients that gets scaled up until either the target volume is hit or an ingredient runs out; when one runs out, the solver recalculates a new ratio from what's left and starts the next phase. Build the pile on the pad phase by phase, in order, using the listed amounts.
- **Print Operations Sheet** — opens your browser's print dialog with a clean, field-ready printout (navigation and buttons are hidden automatically).
- **Save New Recipe / Update Existing Recipe / Save as Copy** — name it and save it to your Recipe Book.

### 5. Docs & FAQ
In-app reference covering:
- **Full User Guide** — a link out to this README, rendered on GitHub.
- How to move recipes between devices (export/import via AirDrop or Nearby Share).
- **Troubleshooting: why can't I see my prior recipes or ingredients?** — covers the browser-scoped storage caveat below.
- What the Structural Index means and why the average must stay above 5.0.
- The math behind the solver (see below).

### 6. 🐛 Report Bugs
A structured bug report form, mirroring [GitHub's recommended issue-form format](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/syntax-for-issue-forms) (Title, Version, Steps to Reproduce, Error Logs). Filling it out and clicking **Submit** opens a pre-filled GitHub issue in a new tab — nothing is sent anywhere automatically, and no data leaves your browser until you actually click "Submit new issue" on GitHub's page (which requires a free GitHub account). This tab notes that the project may not be actively maintained.

## How the Solver Works

- **Canonical metric backend** — internally, all math runs in cubic meters, kg/m³, and kilograms, regardless of what unit you have selected. Every other unit (cubic yards, feet, lb/yd³, wheelbarrows, buckets, US tons) is converted to/from those canonical values only at the display/input boundary. This keeps the core formulas simple and makes the two unit systems fully interoperable — solving the same physical batch in imperial or metric produces the same underlying result.
- **Strict-to-relaxed priority weighting** — your drag-and-drop order assigns penalty weights (1000 / 100 / 10) to deviations from the moisture, density, and C:N targets. The top-ranked metric dominates the search, so it's satisfied first if a perfect blend isn't possible.
- **Stochastic hill-climbing** — rather than a heavy linear/matrix solver, the app randomly nudges the ingredient ratio (in 5% steps, up to 5,000 iterations) and keeps any change that lowers the total penalty score, until it converges or runs out of iterations.
- **Multi-phase fractional optimization** — the pile is built in phases to respect hard inventory caps. Each phase finds the best ratio for the ingredients still available, scales it up until one of them is exhausted, then starts a new phase with whatever's left. This mirrors how you'd actually build a pile on the pad as feedstocks run out.

## Data & Privacy

Everything lives entirely in your browser, tied to that specific browser + device:
- Saved recipes → browser `IndexedDB`.
- Custom ingredient library, dark mode preference, and linked backup file → browser `localStorage`/`IndexedDB`.

Nothing is sent to a server. This data **will not appear** if you open the calculator in a different browser, a different device/user account, an incognito/private window, or after clearing that browser's site data — it isn't synced anywhere by default. Use **Export All** (Recipe Book tab) periodically to back up your recipes and to move them to another browser/device via **Import**.

### Automatic File Backup (Chrome, Edge, Opera)

On Chromium-based browsers, the first time you save a recipe you'll be prompted to pick (or create) a `.json` backup file on disk. From then on, every save/update/delete/note/import silently rewrites that file with your full, current recipe book — no more manual Export clicks. The Recipe Book tab shows the linked filename and lets you unlink or reconnect it at any time.

This relies on the [File System Access API](https://developer.chrome.com/docs/capabilities/web-apis/file-system-access), which **Firefox has explicitly declined to implement** (citing security concerns) and **Safari has never supported**. On those browsers the calculator falls back to the manual Export/Import flow above, and a one-time notice explains that automatic backup needs a Chromium-based browser. Because of this, **the calculator is designed to work best in Chrome, Edge, or Opera** — it's fully usable elsewhere, just without the automatic file sync.

Note this isn't a "save on close" mechanism — browsers don't reliably let a page finish an async file write while it's being closed, so instead the app writes the backup file continuously, immediately after every change, so it's always current.

## Reporting Bugs

Use the in-app **🐛 Report Bugs** tab, or [open an issue directly on GitHub](https://github.com/Alex-G-Strong/Alex-Strongs-Compost-Calculator/issues/new/choose) — both use the same structured template at [`.github/ISSUE_TEMPLATE/bug_report.yml`](.github/ISSUE_TEMPLATE/bug_report.yml).

## Repo Contents

The root is kept to just what the live app needs. Everything else — source data, generator scripts, and dev notes — lives in [`dev/`](dev/).

| File | Purpose |
|---|---|
| [`alexs-compost-calculator_v2.html`](alexs-compost-calculator_v2.html) | The app itself — open this in a browser. This is the only file the live site actually serves. |
| [`.github/ISSUE_TEMPLATE/bug_report.yml`](.github/ISSUE_TEMPLATE/bug_report.yml) | GitHub's structured issue-form template; also mirrored by the in-app Report Bugs tab. |
| [`documentation/`](documentation/) | Copy of this README, kept for reference alongside future docs. |
| [`dev/categorized_compost_database.csv`](dev/categorized_compost_database.csv) | Source data for the 134-item Reference Database in the in-app Ingredient Library (name, category, C:N, bulk density, moisture). |
| [`dev/feedstock_array.js.txt`](dev/feedstock_array.js.txt) | Generated JS array built from the CSV via `gen_feedstock.py` — mirrors exactly what's embedded as `csvLibrary` in the HTML file. If you edit the CSV, rerun the script (from inside `dev/`) and paste the output back into the HTML. |
| [`dev/gen_feedstock.py`](dev/gen_feedstock.py) | Script that converts the CSV into the JS array above (converts density to canonical kg/m³, dedupes by name). |
| [`dev/compostcalc_full_database.png`](dev/compostcalc_full_database.png) | Reference image of the full feedstock database. |
| [`dev/READ_ME_compost-optimizer.md`](dev/READ_ME_compost-optimizer.md) | Developer-facing architecture notes. |
