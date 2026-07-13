const fs = require("fs");
const path = require("path");

const cvPath = process.env.CV_PATH;
const indexPath = path.join(cvPath, "index.html");
let html = fs.readFileSync(indexPath, "utf-8");

// Step1: 全エントリを抽出
const entryRegex = /\{no:(\d+),name:"([^"]*)",file:"([^"]*)",photo:"([^"]*)",dept:"([^"]*)"\}/g;
let entries = [];
let m;
while ((m = entryRegex.exec(html)) !== null) {
  entries.push({ no: parseInt(m[1]), name: m[2], file: m[3], photo: m[4], dept: m[5], full: m[0] });
}
console.log("Total entries:", entries.length);

// No.63 (Khin Khin Thi (2)) を特定
const idx63 = entries.findIndex(e => e.no === 63 && e.name === "Khin Khin Thi (2)");
console.log("No.63 index in array:", idx63);
console.log("No.63 entry:", entries[idx63]);

// Step2: No.63を削除
entries.splice(idx63, 1);
console.log("After delete, total:", entries.length);

// Step3: 63以降のnoを-1（エントリ配列内のno番号をリナンバリング）
// 削除後のidx63以降のエントリのnoを-1
for (let i = idx63; i < entries.length; i++) {
  entries[i].no = entries[i].no - 1;
}

// Step4: ファイル名のナンバリングも調整（削除エントリ以降のみ）
// 元のファイル名の064_〜169_ を 063_〜168_ に変更
// まず元の番号を確認してリネーム対象を特定
const renames = []; // {oldNum, newNum, oldFile, oldPhoto}
for (let i = idx63; i < entries.length; i++) {
  const e = entries[i];
  const oldFileNum = e.no + 1; // 削除前の番号
  const newFileNum = e.no;     // 削除後の番号
  const oldNumStr = String(oldFileNum).padStart(3, "0");
  const newNumStr = String(newFileNum).padStart(3, "0");
  
  // ファイルパスの先頭番号を更新
  const newFile = e.file.replace(/^pdfs\/\d{3}_/, `pdfs/${newNumStr}_`);
  const newPhoto = e.photo.replace(/^photos\/\d{3}_/, `photos/${newNumStr}_`);
  
  if (e.file !== newFile || e.photo !== newPhoto) {
    renames.push({ oldFile: e.file, newFile, oldPhoto: e.photo, newPhoto });
  }
  entries[i].file = newFile;
  entries[i].photo = newPhoto;
}

console.log("Rename count:", renames.length);
console.log("Sample renames (first 3):");
renames.slice(0, 3).forEach(r => console.log(" ", r.oldFile, "->", r.newFile));

// Step5: 新しいエントリ文字列を生成してHTMLを再構築
// 元のエントリ文字列を新しい文字列に置換
// まず元のエントリ一覧（削除含む）をHTMLから抽出して順番通りに置換

// 元のdata配列部分を新しいものに置換
const oldEntryStrings = [];
const newEntryStrings = [];

// 元HTML全エントリを再抽出（削除前）
const originalEntries = [];
const re2 = /\{no:(\d+),name:"([^"]*)",file:"([^"]*)",photo:"([^"]*)",dept:"([^"]*)"\}/g;
let m2;
while ((m2 = re2.exec(html)) !== null) {
  originalEntries.push(m2[0]);
}

// 新エントリを文字列化
const newEntryStrsMap = entries.map(e => 
  `{no:${e.no},name:"${e.name}",file:"${e.file}",photo:"${e.photo}",dept:"${e.dept}"}`
);

// 置換: 元の全エントリ文字列を新しい文字列列に差し替え
// 元エントリを結合した文字列で置換
const oldBlock = originalEntries.join(",\n  ");
const newBlock = newEntryStrsMap.join(",\n  ");

if (html.includes(oldBlock)) {
  html = html.replace(oldBlock, newBlock);
  console.log("Block replacement: OK");
} else {
  console.log("Block not found, trying individual replacement...");
  // フォールバック: 1件ずつ
  // No.63を削除
  html = html.replace(",\n  " + originalEntries[idx63], "");
  // 以降のエントリを更新
  for (let i = idx63; i < originalEntries.length; i++) {
    html = html.replace(originalEntries[i], newEntryStrsMap[i - 1]);
  }
  console.log("Individual replacement done");
}

// バックアップ保存
fs.writeFileSync(path.join(cvPath, "index.html.bak"), fs.readFileSync(indexPath));
// 新HTML保存
fs.writeFileSync(indexPath, html, "utf-8");
console.log("Saved index.html");

// 確認
const verify = [];
const re3 = /\{no:(\d+),name:"([^"]*)",/g;
let m3;
while ((m3 = re3.exec(html)) !== null) {
  if (parseInt(m3[1]) >= 61 && parseInt(m3[1]) <= 66) {
    verify.push(`no:${m3[1]} name:${m3[2]}`);
  }
}
console.log("Verify 61-66:", verify.join(", "));
console.log("DONE");

// リネームリストを出力
console.log("=RENAMES=");
renames.forEach(r => console.log(r.oldFile + "|" + r.newFile + "|" + r.oldPhoto + "|" + r.newPhoto));