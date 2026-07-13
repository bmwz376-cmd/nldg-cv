# -*- coding: utf-8 -*-
import json, re, sys, os
sys.stdout.reconfigure(encoding='utf-8')

# 分類データ読み込み
with open(os.path.join(r'C:\\Users\\NL－DG　PC1\\Desktop\\Work\\nldg-cv', 'dept_results.json'), encoding='utf-8') as f:
    dept_data = {item['no']: item['cat'] for item in json.load(f)}

# index.html読み込み
with open(os.path.join(r'C:\\Users\\NL－DG　PC1\\Desktop\\Work\\nldg-cv', 'index.html'), encoding='utf-8') as f:
    html = f.read()

# candidates配列に dept フィールドを追加
def add_dept(m):
    entry = m.group(0)
    # noを取得
    no_m = re.search(r'no:(\d+)', entry)
    if not no_m: return entry
    no = int(no_m.group(1))
    cat = dept_data.get(no, 'other')
    # dept フィールドを追加（まだない場合）
    if 'dept:' not in entry:
        entry = entry.rstrip('}') + f',dept:"{cat}"}}'
    return entry

html = re.sub(r'\{no:\d+,[^}]+\}', add_dept, html)

# ---- CSS追加（フィルターボタン） ----
filter_css = """
.filter-wrap{margin-bottom:20px;display:flex;flex-wrap:wrap;gap:8px;align-items:center;}
.filter-label{font-size:13px;color:#888;margin-right:4px;}
.btn-filter{background:#fff;border:2px solid #dde3ee;color:#555;padding:8px 16px;border-radius:20px;font-size:13px;font-weight:600;cursor:pointer;transition:all 0.15s;font-family:inherit;}
.btn-filter:hover{border-color:#0D2B5E;color:#0D2B5E;}
.btn-filter.active{background:#0D2B5E;color:#fff;border-color:#0D2B5E;}
.dept-badge{display:inline-block;font-size:10px;font-weight:700;padding:2px 7px;border-radius:4px;margin-bottom:6px;letter-spacing:0.5px;}
.dept-civil{background:#e8f4fd;color:#1565c0;}
.dept-architecture{background:#fff3e0;color:#e65100;}
.dept-electrical{background:#fce4ec;color:#c62828;}
.dept-mechanical{background:#e8f5e9;color:#2e7d32;}
.dept-it{background:#ede7f6;color:#4527a0;}
.dept-other{background:#f5f5f5;color:#757575;}
"""
html = html.replace('.no-result{', filter_css + '.no-result{')

# ---- フィルターUIをsearch-wrapの直後に追加 ----
filter_html = """  <div class="filter-wrap">
    <span class="filter-label">学科：</span>
    <button class="btn-filter active" onclick="setFilter('all')">すべて</button>
    <button class="btn-filter" onclick="setFilter('civil')">🏗 土木</button>
    <button class="btn-filter" onclick="setFilter('architecture')">🏛 建築</button>
    <button class="btn-filter" onclick="setFilter('electrical')">⚡ 電気・電子</button>
    <button class="btn-filter" onclick="setFilter('mechanical')">⚙️ 機械</button>
    <button class="btn-filter" onclick="setFilter('it')">💻 IT・情報</button>
    <button class="btn-filter" onclick="setFilter('other')">📚 その他</button>
  </div>
"""
html = html.replace('  <div class="page-info"', filter_html + '  <div class="page-info"')

# ---- カードにバッジ追加 ----
dept_labels = {
    'civil':'土木', 'architecture':'建築', 'electrical':'電気・電子',
    'mechanical':'機械', 'it':'IT・情報', 'other':'その他'
}
badge_js = """
const deptLabel = {civil:'土木',architecture:'建築',electrical:'電気・電子',mechanical:'機械',it:'IT・情報',other:'その他'};
"""

old_cardfn = "function cardHTML(c) {"
new_cardfn = badge_js + """
function cardHTML(c) {
  const dept = c.dept || 'other';
  const badge = <div class="dept-badge dept-"></div>;"""
html = html.replace(old_cardfn, new_cardfn)

# card-no の前にバッジを挿入
html = html.replace(
    '      <div class="card-no">No.',
    '      \n      <div class="card-no">No.'
)

# ---- JS: フィルター変数と関数追加 ----
old_let = "let filtered = candidates;"
new_let = """let filtered = candidates;
let currentDept = 'all';

function setFilter(dept) {
  currentDept = dept;
  document.querySelectorAll('.btn-filter').forEach(b => b.classList.remove('active'));
  event.target.classList.add('active');
  applyFilters();
}

function applyFilters() {
  const q = document.getElementById('searchBox').value.trim().toLowerCase();
  filtered = candidates.filter(c => {
    const matchDept = currentDept === 'all' || c.dept === currentDept;
    const matchName = !q || c.name.toLowerCase().includes(q);
    return matchDept && matchName;
  });
  currentPage = 1;
  render();
}
"""
html = html.replace(old_let, new_let)

# onSearch を applyFilters に変更
html = html.replace(
    "filtered = q ? candidates.filter(c => c.name.toLowerCase().includes(q)) : candidates;\n  currentPage = 1;\n  render();",
    "applyFilters();"
)

# build meta更新
from datetime import datetime
now = datetime.now().strftime('%Y%m%d-%H%M')
html = re.sub(r'content="20\d{6}-\d{4}"', f'content="{now}"', html)

# 保存
out = os.path.join(r'C:\\Users\\NL－DG　PC1\\Desktop\\Work\\nldg-cv', 'index.html')
with open(out, 'w', encoding='utf-8') as f:
    f.write(html)
print(f'saved: {out}')
print(f'file size: {os.path.getsize(out):,} bytes')

# 検証：deptが全件に入っているか
dept_count = len(re.findall(r'dept:"', html))
no_count   = len(re.findall(r'no:\d+', html))
print(f'candidates: {no_count}件  dept付き: {dept_count}件')
