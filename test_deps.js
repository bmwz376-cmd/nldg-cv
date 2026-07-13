const pdfjsLib = require("pdfjs-dist/legacy/build/pdf.js");
const { createCanvas } = require("canvas");
const fs = require("fs");
const path = require("path");

// canvasモジュールがあるか確認
let canvas;
try {
  canvas = require("canvas");
  console.log("canvas module: OK");
} catch(e) {
  console.log("canvas module: NOT FOUND -", e.message);
}
