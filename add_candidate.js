/**
 * add_candidate.js - 新しい履歴書PDFをnldg-cvサイトに追加
 * 
 * 使い方:
 *   node add_candidate.js <PDFファイルパス> [写真ファイルパス]
 * 例:
 *   node add_candidate.js "C:\Users\...\Downloads\履歴書XXX_merged.pdf"
 *   node add_candidate.js "C:\Users\...\Downloads\履歴書XXX.pdf" "C:\Users\...\photo.jpg"
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const CV_DIR = path.dirname(require.main.filename);
const INDEX_HTML = path.join(CV_DIR, 'index.html');
const PDFS_DIR = path.join(CV_DIR, 'pdfs');
const PHOTOS_DIR = path.join(CV_DIR, 'photos');
const DEFAULT_PHOTO = path.join(PHOTOS_DIR, '034_face.jpg');

// 学科キーワードマッピング
const DEPT_MAP = [
  { keywords: ['機械','mechanical','mechan','エンジン','engine','generator','動力','motor','熱力学','流体'], dept: 'mechanical', label: '機械' },
  { keywords: ['it','情報','computer','software','information technology','computing','プログラム','database'], dept: 'it', label: 'IT・情報' },
  { keywords: ['電気','electrical','electric','電子','electronic','通信','telecommun','回路','circuit'], dept: 'electrical', label: '電気・電子' },
  { keywords: ['建築','architect','building','interior','インテリア'], dept: 'architecture', label: '建築' },
  { keywords: ['土木','civil','構造','structure','施工','construction','道路','橋','コンクリート'], dept: 'civil', label: '土木' },
];

function detectDept(text) {
  const lower = text.toLowerCase();
  for (const { keywords, dept, label } of DEPT_MAP) {
    for (const kw of keywords) {
      if (lower.includes(kw)) return { dept, label };
    }
  }
  return { dept: 'other', label: 'その他' };
}

function getNextNo(html) {
  const matches = [...html.matchAll(/\{no:(\d+),/g)];
  if (!matches.length) return 1;
  return Math.max(...matches.map(m => parseInt(m[1]))) + 1;
}

function zeroPad(n, len = 3) {
  return String(n).padStart(len, '0');
}

async function main() {
  const args = process.argv.slice(2);
  if (!args.length) {
    console.error('使い方: node add_candidate.js <PDFパス> [写真パス]');
    process.exit(1);
  }

  const pdfSrc = args[0];
  const photoSrc = args[1] || null;

  if (!fs.existsSync(pdfSrc)) {
    console.error('PDFが見つかりません: ' + pdfSrc);
    process.exit(1);
  }

  console.log('\n📄 PDF解析中: ' + path.basename(pdfSrc));
  console.log('━'.repeat(55));

  // gsk summarize でPDF解析
  let gskResult = '';
  try {
    gskResult = execSync(
      `gsk summarize "${pdfSrc}" --question "1) Full name of this person (romanized English). 2) Their major/department (mechanical, civil, architecture, electrical, IT, or other). 3) Key technical keywords from their field. Format: NAME: xxx / DEPT: xxx / KEYWORDS: xxx"`,
      { encoding: 'utf8', timeout: 90000 }
    );
    console.log('gsk解析結果:');
    // answerの行だけ抽出して表示
    const lines = gskResult.split('\n').filter(l => l.includes('NAME:') || l.includes('DEPT:') || l.includes('KEYWORDS:') || l.includes('answer'));
    lines.forEach(l => console.log('  ' + l.trim()));
  } catch (e) {
    console.error('gsk解析エラー:', e.message.substring(0, 200));
  }

  // 名前抽出
  let detectedName = '';
  const nameMatch = gskResult.match(/NAME:\s*([A-Za-z][A-Za-z\s]+?)(?:\s*\/|\s*\n|$)/i);
  if (nameMatch) {
    detectedName = nameMatch[1].trim().replace(/\s+/g, ' ');
  }
  // PDFファイル名からフォールバック
  if (!detectedName) {
    const base = path.basename(pdfSrc, '.pdf')
      .replace(/履歴書|resume|cv|_merged|merged/gi, '')
      .replace(/[_\-]/g, ' ').trim();
    detectedName = base || ('Candidate' + getNextNo(fs.readFileSync(INDEX_HTML,'utf-8')));
    console.log('⚠️  名前フォールバック: ' + detectedName);
  }

  // 学科抽出
  const deptMatch = gskResult.match(/DEPT:\s*([^\n\/]+)/i);
  const kwMatch = gskResult.match(/KEYWORDS:\s*([^\n]+)/i);
  const allText = [deptMatch?.[1]||'', kwMatch?.[1]||'', gskResult].join(' ');
  const detectedDept = detectDept(allText);

  const html = fs.readFileSync(INDEX_HTML, 'utf-8');
  const nextNo = getNextNo(html);
  const noStr = zeroPad(nextNo);

  console.log('');
  console.log('✅ No.     : ' + nextNo);
  console.log('✅ 名前   : ' + detectedName);
  console.log('✅ 学科   : ' + detectedDept.label + ' (' + detectedDept.dept + ')');

  // PDFコピー
  const pdfDstName = `${noStr}_${detectedName}.pdf`;
  fs.copyFileSync(pdfSrc, path.join(PDFS_DIR, pdfDstName));
  console.log('📋 PDF    : ' + pdfDstName);

  // 写真コピー
  const photoDstName = `${noStr}_${detectedName}.jpg`;
  if (photoSrc && fs.existsSync(photoSrc)) {
    fs.copyFileSync(photoSrc, path.join(PHOTOS_DIR, photoDstName));
    console.log('🖼️  写真   : ' + photoDstName + ' (指定ファイル)');
  } else {
    fs.copyFileSync(DEFAULT_PHOTO, path.join(PHOTOS_DIR, photoDstName));
    console.log('🖼️  写真   : ' + photoDstName + ' (仮写真 ※後で差し替え可)');
  }

  // index.htmlにエントリ追加
  const newEntry = `{no:${nextNo},name:"${detectedName}",file:"pdfs/${pdfDstName}",photo:"photos/${photoDstName}",dept:"${detectedDept.dept}"}`;

  // 末尾エントリを見つけて追加
  const insertRe = /(\{no:\d+,name:"[^"]+",file:"[^"]+",photo:"[^"]+",dept:"[^"]+"\})(\s*\r?\n\s*\];)/;
  let newHtml;
  if (insertRe.test(html)) {
    newHtml = html.replace(insertRe, `$1,\n  ${newEntry}$2`);
  } else {
    console.error('❌ candidates配列末尾が見つかりません');
    process.exit(1);
  }

  // ビルドスタンプ更新
  const now = new Date(Date.now() + 9*3600000);
  const stamp = `${now.getUTCFullYear()}${String(now.getUTCMonth()+1).padStart(2,'0')}${String(now.getUTCDate()).padStart(2,'0')}-${String(now.getUTCHours()).padStart(2,'0')}${String(now.getUTCMinutes()).padStart(2,'0')}`;
  newHtml = newHtml.replace(/name="build" content="[^"]+"/, `name="build" content="${stamp}"`);

  fs.writeFileSync(INDEX_HTML, newHtml, 'utf-8');

  const newCount = [...newHtml.matchAll(/\{no:(\d+),/g)].length;

  console.log('');
  console.log('━'.repeat(55));
  console.log('🎉 登録完了！ 総件数: ' + newCount + '名');
  console.log('');
  console.log('次のステップ（コピーして実行）:');
  console.log(`  git add -A && git commit -m "Add No.${nextNo} ${detectedName} (${detectedDept.label})" && git push origin main`);
}

main().catch(e => { console.error(e); process.exit(1); });