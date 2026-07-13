import fitz
import cv2
import numpy as np
import os, sys

pdf_dir = sys.argv[1]
out_dir = sys.argv[2]
os.makedirs(out_dir, exist_ok=True)

def extract_face_from_pdf(pdf_path, out_path):
    try:
        doc = fitz.open(pdf_path)
        page = doc[0]
        images = page.get_images(full=True)
        
        best = None
        best_area = 0
        for img_info in images:
            xref = img_info[0]
            try:
                base = doc.extract_image(xref)
                w, h = base["width"], base["height"]
                area = w * h
                ratio = h / max(w, 1)
                if 50*50 < area < 700*900 and 0.7 < ratio < 2.8 and area > best_area:
                    best_area = area
                    best = base
            except:
                continue
        
        if best:
            # cv2でバイト列を直接デコード（tmpファイル不要）
            img_bytes = np.frombuffer(best["image"], dtype=np.uint8)
            img = cv2.imdecode(img_bytes, cv2.IMREAD_COLOR)
            
            if img is None:
                # JPEGデコード失敗時はfitzで展開
                pix = fitz.Pixmap(fitz.open("pdf", doc.tobytes()), best["image"] if False else 0)
                raise ValueError("imdecode failed")
            
            h, w = img.shape[:2]
            if h > w:
                y0 = int((h - w) * 0.05)
                img = img[y0:y0+w, 0:w]
            elif w > h:
                x0 = (w - h) // 2
                img = img[0:h, x0:x0+h]
            
            img = cv2.resize(img, (240, 240), interpolation=cv2.INTER_LANCZOS4)
            cv2.imwrite(out_path, img, [cv2.IMWRITE_JPEG_QUALITY, 92])
            return "IMAGE(%dx%d)" % (best["width"], best["height"])
        
        # フォールバック: ページをレンダリングして右上クロップ
        mat = fitz.Matrix(3, 3)
        pix = page.get_pixmap(matrix=mat)
        arr = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.h, pix.w, pix.n)
        if pix.n == 4:
            arr = cv2.cvtColor(arr, cv2.COLOR_BGRA2BGR)
        elif pix.n == 3:
            arr = cv2.cvtColor(arr, cv2.COLOR_RGB2BGR)
        H, W = arr.shape[:2]
        x1, y1 = int(W*0.68), int(H*0.03)
        x2, y2 = int(W*0.97), int(H*0.30)
        crop = arr[y1:y2, x1:x2]
        ch, cw = crop.shape[:2]
        side = min(ch, cw)
        crop = crop[0:side, 0:side]
        crop = cv2.resize(crop, (240, 240), interpolation=cv2.INTER_LANCZOS4)
        cv2.imwrite(out_path, crop, [cv2.IMWRITE_JPEG_QUALITY, 92])
        return "FALLBACK"
    except Exception as e:
        return "ERROR: " + str(e)

pdfs = sorted([f for f in os.listdir(pdf_dir) if f.endswith('.pdf')])
ok = 0; fb = 0; err = 0
for i, fname in enumerate(pdfs):
    result = extract_face_from_pdf(
        os.path.join(pdf_dir, fname),
        os.path.join(out_dir, fname.replace('.pdf', '.jpg'))
    )
    if "IMAGE" in result: ok += 1
    elif "FALLBACK" in result: fb += 1
    else: err += 1
    sys.stdout.buffer.write(("[%03d/%03d] %s | %s\n" % (i+1, len(pdfs), result, fname)).encode('utf-8'))
    sys.stdout.flush()

sys.stdout.buffer.write(("\n=== DONE: OK=%d FALLBACK=%d ERROR=%d / TOTAL=%d ===\n" % (ok, fb, err, len(pdfs))).encode('utf-8'))