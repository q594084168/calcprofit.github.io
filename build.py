#!/usr/bin/env python3
"""ProfitCalc Build — Profit calculators for eCommerce sellers"""

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

DOMAIN = "calcprofit.net"

def w(path, content):
    full = os.path.join(".", path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)

def build_page(s, is_home=False):
    title = s.get("title", "")
    desc = s.get("desc", "")
    slug = s.get("slug", "")
    fields = s.get("fields", [])  # [{id, label, placeholder, prefix, suffix}]
    formula_text = s.get("formula", "")

    field_html = ""
    for f in fields:
        fid = f["id"]
        label = f.get("label", fid)
        placeholder = f.get("placeholder", "")
        prefix = f.get("prefix", "")
        suffix = f.get("suffix", "")
        field_html += f'''<div class="field">
            <label for="{fid}">{label}</label>
            <div class="input-wrap">
                {f'<span class="prefix">{prefix}</span>' if prefix else ''}
                <input id="{fid}" placeholder="{placeholder}" type="number" step="0.01" oninput="calc()">
                {f'<span class="suffix">{suffix}</span>' if suffix else ''}
            </div>
        </div>'''

    result_html = s.get("results", [])
    result_cards = ""
    if result_html:
        result_cards = '<div class="result-grid">'
        for r in result_html:
            rid = r["id"]
            rlabel = r["label"]
            rprefix = r.get("prefix", "$")
            result_cards += f'''<div class="result-card">
                <div class="result-label">{rlabel}</div>
                <div class="result-value" id="{rid}">{rprefix}0.00</div>
            </div>'''
        result_cards += '</div>'

    platform_cards = ""
    if is_home:
        platform_cards = '<div class="tool-grid">'
        for p in PLATFORMS:
            platform_cards += f'''<a href="/{p["slug"]}/" class="tool-card">
                <h3>{p["title"]}</h3>
                <p>{p["desc"][:80]}...</p>
            </a>'''
        platform_cards += '</div>'

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{desc}">
    <meta name="robots" content="index, follow">
    <meta property="og:title" content="{title} | ProfitCalc">
    <meta property="og:description" content="{desc}">
    <link rel="canonical" href="https://{DOMAIN}/{slug}/">
    <title>{title} | ProfitCalc</title>
    <link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root{{--bg:#FFF8F0;--card:#FFFDFA;--border:#F3E8D8;--text:#1C1917;--muted:#78716C;--primary:#D97706;--primary-hover:#B45309;--radius:16px}}
        *{{box-sizing:border-box;margin:0;padding:0}}
        body{{font-family:'DM Sans',-apple-system,sans-serif;background:var(--bg);color:var(--text);line-height:1.6}}
        nav{{position:sticky;top:0;background:#FFFAF5;backdrop-filter:blur(8px);border-bottom:1px solid var(--border);padding:14px 24px;display:flex;justify-content:space-between;z-index:100}}
        .logo{{font-weight:700;color:var(--primary);font-size:1.2rem;text-decoration:none}}
        .nav-links{{display:flex;gap:20px;align-items:center}}
        .nav-links a{{color:var(--muted);text-decoration:none;font-size:0.9rem;font-weight:500}}
        .nav-links a:hover{{color:var(--text)}}
        .container{{max-width:1100px;margin:0 auto;padding:0 24px}}
        .hero{{text-align:center;padding:48px 0 32px}}
        .hero h1{{font-size:2rem;font-weight:700;margin-bottom:12px;letter-spacing:-0.02em}}
        .hero p{{color:var(--muted);max-width:560px;margin:0 auto;font-size:1rem}}
        .tool-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin:32px 0 48px}}
        @media(max-width:768px){{.tool-grid{{grid-template-columns:1fr}}}} 
        .tool-card{{background:var(--card);border:1px solid var(--border);border-radius:var(--radius);padding:20px;text-decoration:none;color:var(--text);transition:all .15s;box-shadow:0 1px 3px rgba(0,0,0,0.04)}}
        .tool-card:hover{{border-color:var(--primary);box-shadow:0 4px 12px rgba(217,119,6,0.12);transform:translateY(-2px)}}
        .tool-card h3{{font-size:1.05rem;margin-bottom:6px}}
        .tool-card p{{font-size:0.85rem;color:var(--muted)}}
        .calc-section{{max-width:680px;margin:0 auto;padding:40px 0}}
        .calc-card{{background:var(--card);border:1px solid var(--border);border-radius:var(--radius);padding:28px;box-shadow:0 2px 8px rgba(0,0,0,0.05)}}
        .field{{margin-bottom:14px}}
        .field label{{display:block;font-size:0.85rem;font-weight:600;margin-bottom:4px;color:var(--text)}}
        .input-wrap{{display:flex;align-items:center;border:1px solid var(--border);border-radius:10px;overflow:hidden;background:var(--bg);transition:border-color .15s}}
        .input-wrap:focus-within{{border-color:var(--primary)}}
        .prefix,.suffix{{padding:10px 12px;background:#F5F1EB;color:var(--muted);font-size:0.9rem;font-weight:500;white-space:nowrap}}
        .input-wrap input{{flex:1;border:none;padding:10px 12px;background:transparent;color:var(--text);font-family:inherit;font-size:1rem;outline:none;min-width:0}}
        .result-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-top:20px;padding-top:20px;border-top:1px solid var(--border)}}
        @media(max-width:640px){{.result-grid{{grid-template-columns:1fr}}}}
        .result-card{{text-align:center;padding:14px;background:var(--bg);border-radius:10px}}
        .result-label{{font-size:0.8rem;color:var(--muted);margin-bottom:4px}}
        .result-value{{font-size:1.5rem;font-weight:700;color:var(--primary)}}
        .content-section{{max-width:680px;margin:40px auto;padding:0 24px}}
        .content-section h2{{font-size:1.2rem;margin:24px 0 10px}}
        .content-section p{{color:var(--muted);margin-bottom:12px;font-size:0.95rem;line-height:1.7}}
        .cross-link{{margin:40px auto;max-width:680px;padding:20px;background:#FFF7ED;border:1px solid var(--primary);border-radius:12px}}
        .cross-link strong{{color:var(--primary)}}
        .cross-link a{{color:var(--primary);font-weight:500}}
        .breadcrumb{{font-size:0.85rem;color:var(--muted);margin-bottom:16px}}
        .breadcrumb a{{color:var(--primary);text-decoration:none}}
        footer{{background:#1C1917;color:#A8A29E;padding:32px;text-align:center;font-size:0.85rem;margin-top:60px}}
        footer a{{color:#FB923C;text-decoration:none}}
    </style>
    <script type="application/ld+json">
    {{"@context":"https://schema.org","@type":"SoftwareApplication","name":"{title}","url":"https://{DOMAIN}/{slug}/","description":"{desc}","applicationCategory":"FinanceApplication","operatingSystem":"All","offers":{{"@type":"Offer","price":"0","priceCurrency":"USD"}}}}
    </script>
    <script type="application/ld+json">
    {{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{{"@type":"Question","name":"How do I calculate profit margin?","acceptedAnswer":{{"@type":"Answer","text":"Profit margin = (Revenue - Total Costs) / Revenue × 100. Use our free calculator above."}}}},{{"@type":"Question","name":"Is ProfitCalc free?","acceptedAnswer":{{"@type":"Answer","text":"Yes, completely free. No sign-up required. Calculate unlimited profits."}}}},{{"@type":"Question","name":"What platforms does ProfitCalc support?","acceptedAnswer":{{"@type":"Answer","text":"Amazon FBA, Etsy, eBay, Shopify, Dropshipping, and general business profit calculation."}}}}]}}
    </script>
    <script type="application/ld+json">
    {{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{{"@type":"ListItem","position":1,"name":"Home","item":"https://{DOMAIN}/"}},{{"@type":"ListItem","position":2,"name":"{title}","item":"https://{DOMAIN}/{slug}/"}}]}}
    </script>
</head>
<body>
    <nav>
        <a href="/" class="logo">ProfitCalc</a>
        <div class="nav-links">
            <a href="/">Home</a>
            <a href="#calculator">Calculator</a>
            <a href="#faq">FAQ</a>
        </div>
    </nav>
    {f'<div class="container hero"><h1>{title}</h1><p>{desc}</p></div>' if is_home else f'<div class="container"><div class="breadcrumb"><a href="/">Home</a> / {title}</div><h1 style="font-size:1.75rem;font-weight:700;margin:24px 0 8px">{title}</h1><p style="color:var(--muted);margin-bottom:24px">{desc}</p></div>'}
    {platform_cards}
    <div class="calc-section" id="calculator">
        <div class="calc-card">
            {field_html}
            {result_cards}
        </div>
    </div>
    <div class="content-section">
        <h2>What is ProfitCalc?</h2>
        <p>ProfitCalc is a free profit calculator for eCommerce sellers. Calculate your profit margins, fees, and ROI for Amazon FBA, Etsy, eBay, Shopify, and dropshipping businesses. Use ProfitCalc to make smarter pricing decisions — your go-to profit calculator for online sellers.</p>
        <h2>How It Works</h2>
        <p>Step 1: Enter your selling price and cost. Step 2: Add platform fees, shipping, and ad costs. Step 3: Instantly see your profit, margin, and ROI. It's that simple.</p>
        <h2>Common Use Cases</h2>
        <p>ProfitCalc is used by Amazon FBA sellers, Etsy shop owners, eBay resellers, Shopify merchants, and dropshipping entrepreneurs to calculate profitability before listing products.</p>
        {f'<h2>About {title}</h2><p>{desc} Built for sellers who need accurate profit calculations fast.</p>' if not is_home else ''}
    </div>
    <div class="cross-link">
        <strong>Recommended Tools</strong> — Start selling online: <a href="https://www.shopify.com/free-trial" rel="nofollow sponsored">Shopify Free Trial</a>. Scale your Amazon business: <a href="https://www.helium10.com" rel="nofollow sponsored">Helium 10</a>. Need a store built? <a href="https://www.fiverr.com/search/gigs?query=shopify+store+builder" rel="nofollow sponsored">Fiverr Store Builders</a>. Also try our free tools: <a href="https://tracklinks.net">TrackLinks</a> for UTM tracking, <a href="https://compressnow.net">CompressNow</a> for image compression. Optimize your entire seller workflow with our free tool suite.
    </div>
    <div class="content-section" id="faq">
        <h2>Frequently Asked Questions</h2>
        <p><strong>Q: How accurate is the profit calculation?</strong><br>A: The calculator uses the standard profit formula. Actual platform fees may vary — always verify with your platform's fee schedule.</p>
        <p><strong>Q: Is ProfitCalc free?</strong><br>A: Yes, 100% free with no sign-up and no limits on calculations.</p>
        <p><strong>Q: Can I use this for my Amazon FBA business?</strong><br>A: Yes — our Amazon FBA calculator includes FBA fees, referral fees, and PPC ad costs.</p>
        <p><strong>Q: What's the difference between profit margin and ROI?</strong><br>A: Profit margin = Profit / Revenue. ROI = Profit / Investment Cost. Both are useful — margin tells you pricing efficiency, ROI tells you return on your capital.</p>
    </div>
    <footer>
        <p>ProfitCalc — Free Profit Calculator for eCommerce Sellers. Amazon, Etsy, eBay, Shopify, Dropshipping.</p>
        <p style="margin-top:8px"><a href="/">Home</a> · <a href="https://compressnow.net">CompressNow</a> · <a href="https://tracklinks.net">TrackLinks</a> · <a href="https://resizenow.net">ResizeNow</a></p>
    </footer>
    <script>
    function getVal(id){{return parseFloat(document.getElementById(id).value)||0;}}
    function calc(){{
        {s.get('calc_js', '')}
    }}
    calc();
    </script>
</body>
</html>"""

# ═══ Common calc JS ═══════════════════════════════

PROFIT_CALC_JS = """
var price=getVal('price'),cost=getVal('cost'),shipping=getVal('shipping'),fee=getVal('fee'),ads=getVal('ads');
var revenue=price;
var feeAmt=revenue*(fee/100);
var totalCost=cost+shipping+feeAmt+ads;
var profit=revenue-totalCost;
var margin=revenue>0?(profit/revenue*100):0;
var roi=totalCost>0?(profit/totalCost*100):0;
document.getElementById('profit').innerText='$'+profit.toFixed(2);
document.getElementById('margin').innerText=margin.toFixed(1)+'%';
document.getElementById('roi').innerText=roi.toFixed(1)+'%';
"""

# ═══ Page Definitions ═══════════════════════════════

PLATFORMS = [
    {"slug":"amazon-fba","title":"Amazon FBA Profit Calculator","desc":"Calculate Amazon FBA profits including referral fees, FBA fees, and PPC ad costs. Free tool for Amazon sellers.","fields":[
        {"id":"price","label":"Selling Price","placeholder":"29.99","prefix":"$"},
        {"id":"cost","label":"Product Cost","placeholder":"8.00","prefix":"$"},
        {"id":"shipping","label":"FBA Shipping Cost","placeholder":"3.00","prefix":"$"},
        {"id":"fee","label":"Amazon Referral Fee (%)","placeholder":"15","suffix":"%"},
        {"id":"ads","label":"PPC Ads Cost per Unit","placeholder":"2.00","prefix":"$"},
    ],"results":[
        {"id":"profit","label":"Net Profit","prefix":"$"},
        {"id":"margin","label":"Profit Margin","prefix":""},
        {"id":"roi","label":"ROI","prefix":""},
    ],"formula":"Profit = Price - (Cost + FBA + Referral Fee% + Ads)","calc_js":PROFIT_CALC_JS},
    
    {"slug":"etsy","title":"Etsy Fee & Profit Calculator","desc":"Calculate Etsy profits after listing fees, transaction fees, and payment processing. Free Etsy seller tool.","fields":[
        {"id":"price","label":"Selling Price","placeholder":"25.00","prefix":"$"},
        {"id":"cost","label":"Material & Production Cost","placeholder":"10.00","prefix":"$"},
        {"id":"shipping","label":"Shipping Cost","placeholder":"4.00","prefix":"$"},
        {"id":"fee","label":"Etsy Transaction Fee (%)","placeholder":"6.5","suffix":"%"},
        {"id":"ads","label":"Etsy Ads Cost","placeholder":"0.00","prefix":"$"},
    ],"results":[{"id":"profit","label":"Net Profit","prefix":"$"},{"id":"margin","label":"Profit Margin","prefix":""},{"id":"roi","label":"ROI","prefix":""}],"formula":"Profit = Price - (Cost + Shipping + Etsy Fee% + Ads)","calc_js":PROFIT_CALC_JS},
    
    {"slug":"ebay","title":"eBay Profit Calculator","desc":"Calculate eBay selling profits including final value fees and shipping. Free tool for eBay resellers.","fields":[
        {"id":"price","label":"Selling Price","placeholder":"20.00","prefix":"$"},
        {"id":"cost","label":"Cost of Goods","placeholder":"8.00","prefix":"$"},
        {"id":"shipping","label":"Shipping Cost","placeholder":"5.00","prefix":"$"},
        {"id":"fee","label":"eBay Final Value Fee (%)","placeholder":"13.25","suffix":"%"},
        {"id":"ads","label":"Promoted Listing Cost","placeholder":"0.00","prefix":"$"},
    ],"results":[{"id":"profit","label":"Net Profit","prefix":"$"},{"id":"margin","label":"Profit Margin","prefix":""},{"id":"roi","label":"ROI","prefix":""}],"formula":"Profit = Price - (Cost + Shipping + eBay Fee% + Promoted)","calc_js":PROFIT_CALC_JS},
    
    {"slug":"shopify","title":"Shopify Profit Margin Calculator","desc":"Calculate Shopify store profits after payment processing and app fees. Free tool for Shopify merchants.","fields":[
        {"id":"price","label":"Selling Price","placeholder":"49.99","prefix":"$"},
        {"id":"cost","label":"Product & Fulfillment Cost","placeholder":"20.00","prefix":"$"},
        {"id":"shipping","label":"Shipping Cost","placeholder":"5.00","prefix":"$"},
        {"id":"fee","label":"Payment Processing Fee (%)","placeholder":"2.9","suffix":"%"},
        {"id":"ads","label":"Marketing & App Costs","placeholder":"5.00","prefix":"$"},
    ],"results":[{"id":"profit","label":"Net Profit","prefix":"$"},{"id":"margin","label":"Profit Margin","prefix":""},{"id":"roi","label":"ROI","prefix":""}],"formula":"Profit = Price - (Cost + Shipping + Payment Fee% + Marketing)","calc_js":PROFIT_CALC_JS},
    
    {"slug":"dropshipping","title":"Dropshipping Profit Calculator","desc":"Calculate dropshipping profits including supplier cost, shipping, and ad spend. Free tool for dropshippers.","fields":[
        {"id":"price","label":"Selling Price","placeholder":"39.99","prefix":"$"},
        {"id":"cost","label":"Supplier Cost","placeholder":"12.00","prefix":"$"},
        {"id":"shipping","label":"Shipping & Handling","placeholder":"3.00","prefix":"$"},
        {"id":"fee","label":"Platform Fee (%)","placeholder":"5","suffix":"%"},
        {"id":"ads","label":"Facebook/Google Ads per Unit","placeholder":"8.00","prefix":"$"},
    ],"results":[{"id":"profit","label":"Net Profit","prefix":"$"},{"id":"margin","label":"Profit Margin","prefix":""},{"id":"roi","label":"ROI","prefix":""}],"formula":"Profit = Price - (Supplier Cost + Shipping + Fee% + Ads)","calc_js":PROFIT_CALC_JS},
    
    {"slug":"small-business","title":"Small Business Profit Calculator","desc":"Calculate profit margins for any small business or product. Free profit calculator for entrepreneurs.","fields":[
        {"id":"price","label":"Revenue (Monthly)","placeholder":"10000","prefix":"$"},
        {"id":"cost","label":"Cost of Goods Sold","placeholder":"4000","prefix":"$"},
        {"id":"shipping","label":"Operating Expenses","placeholder":"2000","prefix":"$"},
        {"id":"fee","label":"Tax Rate (%)","placeholder":"20","suffix":"%"},
        {"id":"ads","label":"Marketing Spend","placeholder":"1000","prefix":"$"},
    ],"results":[{"id":"profit","label":"Net Profit","prefix":"$"},{"id":"margin","label":"Profit Margin","prefix":""},{"id":"roi","label":"ROI","prefix":""}],"formula":"Profit = Revenue - (COGS + Operating + Tax% + Marketing)","calc_js":PROFIT_CALC_JS},
]

HOMEPAGE = {"title":"Free Profit Calculator for eCommerce Sellers","desc":"Calculate profit margins, fees, and ROI for Amazon FBA, Etsy, eBay, Shopify, and dropshipping. Free, no sign-up.","slug":"","fields":[
    {"id":"price","label":"Selling Price","placeholder":"29.99","prefix":"$"},
    {"id":"cost","label":"Product Cost","placeholder":"10.00","prefix":"$"},
    {"id":"shipping","label":"Shipping Cost","placeholder":"5.00","prefix":"$"},
    {"id":"fee","label":"Platform Fee (%)","placeholder":"10","suffix":"%"},
    {"id":"ads","label":"Ad Spend per Unit","placeholder":"3.00","prefix":"$"},
],"results":[{"id":"profit","label":"Net Profit","prefix":"$"},{"id":"margin","label":"Profit Margin","prefix":""},{"id":"roi","label":"ROI","prefix":""}],"calc_js":PROFIT_CALC_JS}

ALL_SCENARIOS = PLATFORMS

def build_home():
    html = build_page(HOMEPAGE, is_home=True)
    w("index.html", html)
    print("🏠 index.html")

def build_scenes():
    for s in ALL_SCENARIOS:
        html = build_page(s)
        w(f"{s['slug']}/index.html", html)
        print(f"  📄 {s['slug']}/")

def build_sitemap():
    import os
    urls = [f"https://{DOMAIN}/"]
    for root, dirs, files in os.walk('.'):
        for f in files:
            if f == 'index.html' and root != '.':
                rel = os.path.relpath(root, '.').replace('\\', '/')
                if not rel.startswith('.') and not rel.startswith('.git'):
                    urls.append(f"https://{DOMAIN}/{rel}/")
    lines = ['<?xml version="1.0" encoding="UTF-8"?>']
    lines.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    for u in urls:
        p = "1.0" if u == f"https://{DOMAIN}/" else "0.8"
        lines.append(f'  <url><loc>{u}</loc><changefreq>weekly</changefreq><priority>{p}</priority></url>')
    lines.append('</urlset>')
    with open('sitemap.xml', 'w') as f:
        f.write('\n'.join(lines))
    print(f"📄 sitemap.xml ({len(urls)} URLs)")

def build_robots():
    w("robots.txt", f"User-agent: *\nAllow: /\nSitemap: https://{DOMAIN}/sitemap.xml\n")
    print("🤖 robots.txt")

def build_static():
    w("privacy.html", "<h1>Privacy</h1><p>ProfitCalc does not collect or store personal data. All calculations happen in your browser.</p>")
    w("terms.html", "<h1>Terms</h1><p>Free tool. Calculations are estimates. Verify with your platform.</p>")
    w("contact.html", "<h1>Contact</h1><p>For questions, reach out via the domain contact form.</p>")
    w("404.html", "<h1>404</h1><p>Page not found. <a href='/'>Back to ProfitCalc</a></p>")

if __name__ == "__main__":
    build_home()
    print(f"\n📄 6 Calculator Pages:")
    build_scenes()
    build_sitemap()
    build_robots()
    build_static()
    print(f"\n✅ Build Complete — {len(ALL_SCENARIOS) + 5} pages")
