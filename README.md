# Alex Strong's Compost Calculator

A single-page, offline-capable web app for designing multi-ingredient compost recipes. You tell it what feedstocks you have on hand and how much of each, rank what matters most (moisture, density, or C:N ratio), and it builds a phased "Operations Sheet" telling you exactly how much of each ingredient to load onto the pad.

No install, no server, no internet connection required — just open the HTML file in a browser.

## Quick Start

1. Open [`alexs-compost-calculator_v2.html`](alexs-compost-calculator_v2.html) in any modern browser (Chrome, Edge, Safari, Firefox).
2. Click **+ Start a New Recipe**.
3. Walk through the four tabs in order: **Constraints → Ingredients → Operations Sheet**.
4. Save the result to your Recipe Book so you can reload, print, or annotate it later.

Everything is saved locally in your browser (via `localStorage` and `IndexedDB`) — nothing is uploaded anywhere.

## Walkthrough

### 1. Recipe Book
This is the home tab. It lists every recipe you've saved, showing the date, total volume, and final pile health metrics for each. From here you can:
- **Load Input** — pull a saved recipe back onto the workbench to tweak and re-solve it.
- **+ Note** — attach a dated field note (and optionally a photo) to a recipe, e.g. to log how the pile actually turned out.
- **Export** — download a single recipe as a `.json` file.
- **Export All** — back up your entire recipe book as one `.json` file.
- **Import** — load a `.json` file exported from this app (yours or someone else's). Useful for moving recipes between devices — see the FAQ tab for AirDrop/Nearby Share instructions.
- **✕** — delete a recipe.

Click **+ Start a New Recipe** to clear the workbench and begin.

### 2. Constraints — Site & Batch Settings
Set up the batch before adding ingredients:

- **Measurement Unit** — the physical unit you'll actually use on the pad: Cubic Yards, a custom loader bucket size, Wheelbarrow (~6 cu ft), or 5-Gallon Bucket. All ingredient quantities and results will be shown in this unit.
- **Define Batch Size By** — either:
  - **Direct Volume**: enter a target volume in cubic yards, or
  - **Pile Dimensions**: enter Length × Base Width × Height (ft), and the tool calculates volume using a parabolic pile profile (`Base × Height × 0.67 × Length`). If your height exceeds 5/8 of the base width, it warns you the pile risks over-compaction and will need a high structural index.

**Optimization Priorities & Ranges** — drag the three cards (using the `≡` handle) into the order that matters most to you:
- **Moisture (%)** — target 55–65%. Too dry slows decomposition; too wet goes anaerobic and smells.
- **Density (lb/yd³)** — target 600–800. A proxy for porosity/airflow.
- **C:N Ratio** — target 25–35. The carbon ("browns") to nitrogen ("greens") balance that feeds the microbes.

You can edit the min/max range for each metric. **The solver strictly prioritizes whichever card is on top** — if your feedstocks can't satisfy all three ranges at once, it sacrifices the lowest-ranked one first.

Click **Next: Add Ingredients →** when ready.

### 3. Ingredients
Build your list of available feedstocks. For each row:

- **Ingredient Name** — start typing to autocomplete from the built-in library (Horse Manure, Wood Chips, Grass Clippings, Cow Manure, Poultry Manure, Vegetable Scraps, Coffee Grounds, Dry Leaves, Straw, Cardboard/Paper, Sawdust, Food Waste) or your own saved custom items. Picking a known name auto-fills the fields below.
- **C:N** — carbon-to-nitrogen ratio.
- **Density** — bulk weight in lb/yd³.
- **Moist.** — moisture percentage.
- **Struct.** (Structural Index, 1–10) — resistance to compaction. 10 = rigid (wood chips), 1 = mushy (food waste). See the FAQ tab for why this matters.
- **Avail. Inventory** — the maximum amount you actually have on hand, in whatever unit you chose in Constraints. Leave blank for unlimited. **The solver will never exceed this limit.**

For a feedstock not in the library, fill in the values yourself (lab test results, a web search, or a reasonable estimate) and click **Save to Lib** to reuse it in future recipes. Manage or delete saved custom ingredients any time via **Manage Saved Items**.

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
- How to move recipes between devices (export/import via AirDrop or Nearby Share).
- What the Structural Index means and why the average must stay above 5.0.
- The math behind the solver (see below).

## How the Solver Works

- **Strict-to-relaxed priority weighting** — your drag-and-drop order assigns penalty weights (1000 / 100 / 10) to deviations from the moisture, density, and C:N targets. The top-ranked metric dominates the search, so it's satisfied first if a perfect blend isn't possible.
- **Stochastic hill-climbing** — rather than a heavy linear/matrix solver, the app randomly nudges the ingredient ratio (in 5% steps, up to 5,000 iterations) and keeps any change that lowers the total penalty score, until it converges or runs out of iterations.
- **Multi-phase fractional optimization** — the pile is built in phases to respect hard inventory caps. Each phase finds the best ratio for the ingredients still available, scales it up until one of them is exhausted, then starts a new phase with whatever's left. This mirrors how you'd actually build a pile on the pad as feedstocks run out.

## Data & Privacy

Everything lives entirely in your browser:
- Saved recipes → browser `IndexedDB`.
- Custom ingredient library and dark mode preference → browser `localStorage`.

Nothing is sent to a server. Clearing your browser data will erase saved recipes — use **Export All** periodically to back them up.

## Repo Contents

| File | Purpose |
|---|---|
| [`alexs-compost-calculator_v2.html`](alexs-compost-calculator_v2.html) | The app itself — open this in a browser. |
| [`categorized_compost_database.csv`](categorized_compost_database.csv) | Source feedstock data used to build the ingredient library. |
| [`feedstock_array.js.txt`](feedstock_array.js.txt) | Generated JS array of feedstocks from the CSV. |
| [`gen_feedstock.py`](gen_feedstock.py) | Script that converts the CSV into the JS feedstock array. |
| [`compostcalc_full_database.png`](compostcalc_full_database.png) | Reference image of the full feedstock database. |
| [`READ_ME_compost-optimizer.md`](READ_ME_compost-optimizer.md) | Developer-facing architecture notes. |
