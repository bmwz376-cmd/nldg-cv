const { fromPath } = require("pdf2pic");
const path = require("path");
const fs = require("fs");

const repoDir = process.cwd();
const targets = [
  { pdf: "159_Lae Yi Win.pdf",       jpg: "159_Lae Yi Win.jpg" },
  { pdf: "160_Thuzar Myint.pdf",     jpg: "160_Thuzar Myint.jpg" },
  { pdf: "161_Aye Thandar Aung.pdf", jpg: "161_Aye Thandar Aung.jpg" },
];

(async () => {
  for (const t of targets) {
    const pdfPath = path.join(repoDir, "pdfs", t.pdf);
    const outDir  = path.join(repoDir, "photos_tmp");
    fs.mkdirSync(outDir, { recursive: true });

    console.log("Processing:", t.pdf);
    try {
      const convert = fromPath(pdfPath, {
        density: 150,
        saveFilename: "page",
        savePath: outDir,
        format: "jpg",
        width: 800,
        height: 1131,
      });
      const result = await convert(1, { responseType: "image" });
      // photos_tmp/page.1.jpg -> photos/xxx.jpg
      const tmpFile = path.join(outDir, "page.1.jpg");
      const dstFile = path.join(repoDir, "photos", t.jpg);
      if (fs.existsSync(tmpFile)) {
        fs.copyFileSync(tmpFile, dstFile);
        fs.unlinkSync(tmpFile);
        console.log("  -> Saved:", t.jpg);
      } else {
        console.log("  -> ERROR: page.1.jpg not found");
      }
    } catch(e) {
      console.error("  -> ERROR:", e.message);
    }
  }
})();
