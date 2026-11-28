import os
import shutil
import glob
from datetime import datetime

ROOT = os.getcwd()
SCRIPTS_DIR = os.path.join(ROOT, "scripts")
os.makedirs(SCRIPTS_DIR, exist_ok=True)

# 1. Move loose Python scripts from root into /scripts/
py_files = [
    "cleanup_savingstactic.py",
    "generate_sitemap.py",
    "google_index.py",
    "indexnow_index.py",
    "phase3_upgrade_savingstactic.py",
    "dump.py",
]

for fname in py_files:
    src = os.path.join(ROOT, fname)
    dst = os.path.join(SCRIPTS_DIR, fname)
    if os.path.exists(src):
        shutil.move(src, dst)
        print(f"Moved {fname} -> scripts/{fname}")

# Update workflow paths if .github/workflows exists
for wf in glob.glob(os.path.join(ROOT, ".github", "workflows", "*.yml")):
    with open(wf, "r", encoding="utf-8") as f:
        content = f.read()
    updated = content
    for fname in py_files:
        updated = updated.replace(f"python {fname}", f"python scripts/{fname}")
        updated = updated.replace(f"python3 {fname}", f"python3 scripts/{fname}")
    if updated != content:
        with open(wf, "w", encoding="utf-8") as f:
            f.write(updated)
        print(f"Updated workflow paths in {os.path.basename(wf)}")

# Ensure dump artifacts are ignored in .gitignore
gitignore_path = os.path.join(ROOT, ".gitignore")
ignore_entries = ["scripts/dump.py", "full_repo_dump*.txt", "__pycache__/"]
existing_ignore = ""
if os.path.exists(gitignore_path):
    with open(gitignore_path, "r", encoding="utf-8") as f:
        existing_ignore = f.read()
with open(gitignore_path, "a", encoding="utf-8") as f:
    for entry in ignore_entries:
        if entry not in existing_ignore:
            f.write(f"\n{entry}")

# 2. Shared HTML Page Builder for Clean Hub Pages
def build_hub_page(title, meta_desc, canonical, badge, h1, subtitle, sections_html):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="description" content="{meta_desc}">
    <link rel="canonical" href="{canonical}">
    <meta name="robots" content="index, follow, max-image-preview:large">
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-50 text-gray-800 font-sans antialiased min-h-screen flex flex-col justify-between">
    <header class="bg-white border-b border-gray-200 sticky top-0 z-50 shadow-sm">
        <div class="max-w-6xl mx-auto px-4 py-3.5 flex flex-wrap justify-between items-center gap-3">
            <a href="/" class="flex items-center space-x-2">
                <span class="bg-blue-600 text-white font-black text-xl px-3 py-1 rounded-md tracking-wider">ST</span>
                <span class="text-xl font-bold tracking-tight text-gray-900">Savings<span class="text-blue-600">Tactic</span></span>
            </a>
            <nav class="flex flex-wrap items-center gap-4 text-xs font-bold text-gray-600">
                <a href="/tools/" class="hover:text-emerald-600 transition">Calculators &amp; Tools</a>
                <a href="/tactics/" class="hover:text-blue-600 transition">Money-Saving Tactics</a>
                <a href="/cvs/" class="hover:text-rose-600 transition">CVS Hub</a>
                <a href="/earn/" class="hover:text-purple-600 transition">Cashback &amp; Rewards</a>
                <a href="/blog/" class="bg-gray-900 text-white px-3 py-1.5 rounded-lg hover:bg-gray-800 transition">All Guides</a>
            </nav>
        </div>
    </header>

    <main class="max-w-5xl mx-auto px-4 py-10 flex-grow w-full space-y-10">
        <section class="bg-white rounded-3xl border border-gray-200 p-6 md:p-10 shadow-sm space-y-3">
            <span class="bg-blue-100 text-blue-800 text-[11px] font-black px-3 py-1 rounded-full uppercase tracking-wider">{badge}</span>
            <h1 class="text-2xl md:text-4xl font-extrabold text-gray-900 tracking-tight">{h1}</h1>
            <p class="text-sm text-gray-600 max-w-3xl leading-relaxed">{subtitle}</p>
        </section>
        {sections_html}
    </main>

    <footer class="bg-white border-t border-gray-200 mt-12 py-8">
        <div class="max-w-6xl mx-auto px-4 text-center space-y-3">
            <p class="text-xs text-gray-500 max-w-3xl mx-auto">
                <strong>Advertiser &amp; Editorial Disclosure:</strong> SavingsTactic.com is an independent publisher. As an Amazon Associate, SavingsTactic earns from qualifying purchases. Inquiries: <a href="mailto:partners@savingstactic.com" class="underline">partners@savingstactic.com</a>.
            </p>
            <div class="flex justify-center space-x-6 text-xs text-gray-500 font-semibold">
                <a href="/" class="hover:underline">Home</a>
                <span>&bull;</span>
                <a href="/tools/" class="hover:underline">Tools</a>
                <span>&bull;</span>
                <a href="/tactics/" class="hover:underline">Money-Saving Tactics</a>
                <span>&bull;</span>
                <a href="/privacy.html" class="hover:underline">Privacy Policy</a>
            </div>
            <p class="text-xs text-gray-400">&copy; 2026 SavingsTactic.com &mdash; All Rights Reserved.</p>
        </div>
    </footer>
</body>
</html>"""

def card_grid(items):
    cards = []
    for title, desc, href, tag in items:
        cards.append(f"""
        <a href="{href}" class="bg-white rounded-2xl border border-gray-200 p-5 shadow-sm hover:border-blue-400 hover:shadow transition flex flex-col justify-between space-y-3">
            <div class="space-y-2">
                <span class="bg-gray-100 text-gray-700 text-[10px] font-extrabold px-2.5 py-0.5 rounded uppercase">{tag}</span>
                <h3 class="text-base font-extrabold text-gray-900 leading-snug">{title}</h3>
                <p class="text-xs text-gray-600 leading-relaxed">{desc}</p>
            </div>
            <span class="text-xs font-extrabold text-blue-600">Open Resource &rarr;</span>
        </a>""")
    return f'<div class="grid md:grid-cols-2 lg:grid-cols-3 gap-5">{"".join(cards)}</div>'

tools_items = [
    ("Grocery Unit Price Calculator", "Compare bulk vs. single packages per ounce, pound, or count in the aisle.", "/blog/grocery-unit-price-calculator.html", "Calculator"),
    ("CVS 98% Rule Spend Calculator", "Verify pre-coupon spend thresholds before checking out on ExtraBucks deals.", "/blog/cvs-98-percent-rule-calculator.html", "CVS Tool"),
    ("Household Rebate & Savings Ledger", "Track out-of-pocket register spend separately from pending or paid cashback.", "/blog/grocery-rebate-and-savings-ledger.html", "Interactive Ledger"),
    ("Free 2026 Grocery Price Book Template", "Build custom stock-up price rows and export straight to Excel or Google Sheets.", "/blog/free-grocery-price-book-template.html", "CSV Template"),
    ("Emergency Food & Water Ration Calculator", "Calculate 3-to-90-day water gallons, calories, and DIY pantry costs.", "/blog/emergency-food-water-calculator.html", "Prep Calculator"),
]

tactics_items = [
    ("Dollar General Penny Shopping List 2026", "Decode colored clearance dots, Tuesday markdown drops, and DG app scanning.", "/blog/dollar-general-penny-shopping-clearance-list.html", "Clearance Tactic"),
    ("How to Calculate Shrinkflation", "Spot hidden package downsizing fast with our per-unit shrinkflation formula.", "/blog/how-to-calculate-shrinkflation.html", "Grocery Math"),
    ("Gift Card Stacking for Big Releases & Purchases", "Layer discounted retail gift cards, portal cashback, and rewards on major buys.", "/blog/how-to-get-gta-6-cheaper-gift-card-stacking.html", "Gift Card Stack"),
    ("Budget Storage Expansion Without Overpaying", "Compare cost-per-GB NVMe SSD options for PS5 and Xbox expansion.", "/blog/gta-6-storage-fix-best-ps5-xbox-ssd.html", "Hardware Value"),
    ("Walgreens Cash on Spend Deals", "Avoid accidentally voiding Walgreens Cash boosters when redeeming rewards.", "/blog/how-to-use-walgreens-cash-on-spend-deals.html", "Store Policy"),
    ("Pickup vs. In-Store Digital Coupon Rules", "Side-by-side matrix for CVS, Walgreens, Kroger, and Walmart order channels.", "/blog/pickup-vs-in-store-digital-coupon-rules.html", "Channel Rules"),
    ("How Kroger Fuel Points Work", "Maximize 2x–4x gift card fuel multipliers before they expire.", "/blog/how-do-kroger-fuel-points-work.html", "Fuel Tactic"),
    ("Does Aldi Take Coupons or Price Match?", "Official Aldi coupon, double-guarantee, and price-match policy breakdown.", "/blog/does-aldi-take-coupons-or-price-match.html", "Store Policy"),
    ("Budget Solar Generators for Outages", "Calculate appliance watt-hours and compare LiFePO4 backup power stations.", "/blog/best-budget-solar-generators-power-outage.html", "Off-Grid Value"),
]

# 3. Write /tools/index.html
os.makedirs(os.path.join(ROOT, "tools"), exist_ok=True)
with open(os.path.join(ROOT, "tools", "index.html"), "w", encoding="utf-8") as f:
    f.write(build_hub_page(
        "Free Grocery & Savings Calculators | Savings Tactic",
        "Interactive unit price calculators, CVS 98% spend checkers, household rebate ledgers, and printable price-book templates.",
        "https://www.savingstactic.com/tools/",
        "Interactive Calculators & Templates",
        "Free Savings Calculators &amp; Household Ledgers",
        "Browser-based math tools designed to eliminate guesswork at checkout, track pending rebates, and lock in rock-bottom unit prices.",
        card_grid(tools_items)
    ))

# 4. Write /tactics/index.html
os.makedirs(os.path.join(ROOT, "tactics"), exist_ok=True)
with open(os.path.join(ROOT, "tactics", "index.html"), "w", encoding="utf-8") as f:
    f.write(build_hub_page(
        "Money-Saving Tactics & Store Coupon Rules (2026) | Savings Tactic",
        "Actionable money-saving tactics: gift card stacking, Dollar General penny shopping, shrinkflation math, and store coupon policies.",
        "https://www.savingstactic.com/tactics/",
        "Money-Saving Tactics Hub",
        "Proven Money-Saving Tactics, Store Rules &amp; Stacking Guides",
        "Step-by-step playbooks for stacking gift cards, decoding store coupon policies, catching clearance drops, and cutting household bills.",
        card_grid(tactics_items)
    ))

# 5. Rebuild clean sitemap.xml covering all HTML pages
today = datetime.utcnow().strftime("%Y-%m-%d")
urls = [
    ("https://www.savingstactic.com/", "1.0"),
    ("https://www.savingstactic.com/tools/", "0.9"),
    ("https://www.savingstactic.com/tactics/", "0.9"),
    ("https://www.savingstactic.com/cvs/", "0.9"),
    ("https://www.savingstactic.com/earn/", "0.9"),
    ("https://www.savingstactic.com/blog/", "0.8"),
]

for html_file in sorted(glob.glob(os.path.join(ROOT, "blog", "*.html"))):
    bn = os.path.basename(html_file)
    if bn != "index.html":
        urls.append((f"https://www.savingstactic.com/blog/{bn}", "0.8"))

for static_page in ["about.html", "contact.html", "privacy.html", "terms.html"]:
    if os.path.exists(os.path.join(ROOT, static_page)):
        urls.append((f"https://www.savingstactic.com/{static_page}", "0.4"))

xml_lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for loc, prio in urls:
    xml_lines.append(f"  <url><loc>{loc}</loc><lastmod>{today}</lastmod><priority>{prio}</priority></url>")
xml_lines.append("</urlset>\n")

with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
    f.write("\n".join(xml_lines))

print(f"Done! Created /tools/ and /tactics/ hubs and synced {len(urls)} URLs to sitemap.xml.")
