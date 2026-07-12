"""Regenerates feedstock_array.js.txt from categorized_compost_database.csv.

This mirrors exactly what's embedded as `csvLibrary` in
alexs-compost-calculator_v2.html: density converted from the source CSV's
lb/cy to the app's canonical kg/m3, deduplicated by name (first occurrence
wins). If you edit the CSV, rerun this script, then paste the output back
into the `const csvLibrary = [...]` array in the HTML file.
"""
import csv

cat_si = {
    'Wood & Paper': 8,
    'Straw, Hay & Silage': 7,
    'Yard Trimmings & Vegetation': 5,
    'Crop Residues & Processing Wastes': 4,
    'Manures & Animal Waste': 3,
    'Meat, Fish & Animal By-Products': 2,
    'Food & Municipal Waste': 1,
    'Liquids & Additives': 1,
}

KG_M3_PER_LB_YD3 = 0.593276

def esc(s):
    return s.replace('\\', '\\\\').replace('"', '\\"')

seen = set()
lines = []
with open('categorized_compost_database.csv', encoding='utf-8') as f:
    r = csv.DictReader(f)
    for row in r:
        name = row['Feedstock'].strip()
        if not name or name.lower() in seen:
            continue
        seen.add(name.lower())
        cat = row['Category'].strip()
        cn = float(row['C:N Ratio'].strip())
        density_kgm3 = round(float(row['Bulk Density (lb/cy)'].strip()) * KG_M3_PER_LB_YD3, 1)
        moisture = float(row['Moisture (%)'].strip())
        si = cat_si.get(cat, 5)
        lines.append('        { name: "%s", category: "%s", cn: %g, density: %g, moisture: %g, si: %d }' % (
            esc(name), esc(cat), cn, density_kgm3, moisture, si))

out = ',\n'.join(lines)
with open('feedstock_array.js.txt', 'w', encoding='utf-8') as f:
    f.write(out)
print('wrote', len(lines), 'lines')
