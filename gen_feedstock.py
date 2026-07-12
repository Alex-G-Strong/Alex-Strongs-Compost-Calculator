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

def esc(s):
    return s.replace('\\', '\\\\').replace('"', '\\"')

lines = []
with open('categorized_compost_database.csv', encoding='utf-8') as f:
    r = csv.DictReader(f)
    for row in r:
        name = row['Feedstock'].strip()
        cat = row['Category'].strip()
        cn = float(row['C:N Ratio'].strip())
        density = float(row['Bulk Density (lb/cy)'].strip())
        moisture = float(row['Moisture (%)'].strip())
        si = cat_si.get(cat, 5)
        lines.append('        { name: "%s", category: "%s", cn: %g, density: %g, moisture: %g, si: %d }' % (esc(name), esc(cat), cn, density, moisture, si))

out = ',\n'.join(lines)
with open('feedstock_array.js.txt', 'w', encoding='utf-8') as f:
    f.write(out)
print('wrote', len(lines), 'lines')
