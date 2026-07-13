import fitz, cv2, numpy as np, os, sys

pdf_dir = 'pdfs'
out_dir = 'photos'

def is_face_photo(w, h):
    """顔写真らしいサイズ・縦横比か判定"""
    area = w * h
    ratio = h / max(w, 1)
    # 正方形〜縦長、かつ適切なサイズ（小さすぎず大きすぎず）
    return 0.7 <= ratio <= 2.5 and 2500 < area < 500000

def is_full_page(w, h):
    """ページ全体の大きい画像か判定（これは使わない）"""
    return w * h > 3000000 or (w > 1500 and h > 2000)

def extract_best(pdf_path, out_path):
    doc = fitz.open(pdf_path)
    best = None
    best_score = 0

    for pno in range(len(doc)):
        page = doc[pno]
        imgs = page.get_images(full=True)
        for img_info in imgs:
            xref = img_info[0]
            try:
                base = doc.extract_image(xref)
                w, h = base['width'], base['height']
                if is_full_page(w, h):
                    continue  # ページ全体画像は除外
                if not is_face_photo(w, h):
                    continue
                area = w * h
                ratio = h / max(w, 1)
                # 縦長(1.1-1.8)が理想的な顔写真比率
                ratio_score = 1.5 if 1.1 <= ratio <= 1.8 else 1.0
                score = area * ratio_score
                if pno > 0:
                    score *= 1.1  # 2ページ目以降を少し優先
                if score > best_score:
                    best_score = score
                    best = base
            except:
                continue

    if best:
        img_bytes = np.frombuffer(best['image'], dtype=np.uint8)
        img = cv2.imdecode(img_bytes, cv2.IMREAD_COLOR)
        if img is not None:
            h, w = img.shape[:2]
            if h > w:
                y0 = int((h - w) * 0.05)
                img = img[y0:y0+w, 0:w]
            elif w > h:
                x0 = (w - h) // 2
                img = img[0:h, x0:x0+h]
            img = cv2.resize(img, (240, 240), interpolation=cv2.INTER_LANCZOS4)
            cv2.imwrite(out_path, img, [cv2.IMWRITE_JPEG_QUALITY, 92])
            return 'IMAGE', best['width'], best['height']

    # フォールバック: 1ページ目右上クロップ
    page = doc[0]
    mat = fitz.Matrix(3, 3)
    pix = page.get_pixmap(matrix=mat)
    arr = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.h, pix.w, pix.n)
    if pix.n == 4: arr = cv2.cvtColor(arr, cv2.COLOR_BGRA2BGR)
    elif pix.n == 3: arr = cv2.cvtColor(arr, cv2.COLOR_RGB2BGR)
    H, W = arr.shape[:2]
    crop = arr[int(H*0.03):int(H*0.30), int(W*0.68):int(W*0.97)]
    ch, cw = crop.shape[:2]; side = min(ch, cw)
    crop = crop[0:side, 0:side]
    crop = cv2.resize(crop, (240, 240), interpolation=cv2.INTER_LANCZOS4)
    cv2.imwrite(out_path, crop, [cv2.IMWRITE_JPEG_QUALITY, 92])
    return 'FALLBACK', 0, 0

pdfs = sorted([f for f in os.listdir(pdf_dir) if f.endswith('.pdf')])
ok = 0; fb = 0
for fname in pdfs:
    result, w, h = extract_best(
        os.path.join(pdf_dir, fname),
        os.path.join(out_dir, fname.replace('.pdf', '.jpg'))
    )
    if result == 'IMAGE': ok += 1
    else: fb += 1
    sys.stdout.buffer.write(f'{result}({w}x{h}) | {fname}\n'.encode('utf-8'))
    sys.stdout.flush()

sys.stdout.buffer.write(f'\nOK={ok} FALLBACK={fb}\n'.encode('utf-8'))