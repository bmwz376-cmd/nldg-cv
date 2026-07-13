import fitz, cv2, numpy as np, os, sys

pdf_dir = sys.argv[1]
out_dir = sys.argv[2]
start_no = int(sys.argv[3]) if len(sys.argv) > 3 else 68
os.makedirs(out_dir, exist_ok=True)

def extract(pdf_path, out_path):
    try:
        doc = fitz.open(pdf_path)
        page = doc[0]
        images = page.get_images(full=True)
        best = None; best_area = 0
        for img_info in images:
            xref = img_info[0]
            try:
                base = doc.extract_image(xref)
                w, h = base["width"], base["height"]
                area = w * h
                ratio = h / max(w, 1)
                if 50*50 < area < 700*900 and 0.7 < ratio < 2.8 and area > best_area:
                    best_area = area; best = base
            except: continue
        if best:
            img_bytes = np.frombuffer(best["image"], dtype=np.uint8)
            img = cv2.imdecode(img_bytes, cv2.IMREAD_COLOR)
            if img is None: raise ValueError("decode failed")
            h, w = img.shape[:2]
            if h > w:
                y0 = int((h-w)*0.05); img = img[y0:y0+w, 0:w]
            elif w > h:
                x0 = (w-h)//2; img = img[0:h, x0:x0+h]
            img = cv2.resize(img, (240,240), interpolation=cv2.INTER_LANCZOS4)
            cv2.imwrite(out_path, img, [cv2.IMWRITE_JPEG_QUALITY, 92])
            return "IMAGE"
        mat = fitz.Matrix(3,3); pix = page.get_pixmap(matrix=mat)
        arr = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.h, pix.w, pix.n)
        if pix.n==4: arr=cv2.cvtColor(arr, cv2.COLOR_BGRA2BGR)
        elif pix.n==3: arr=cv2.cvtColor(arr, cv2.COLOR_RGB2BGR)
        H,W=arr.shape[:2]; crop=arr[int(H*0.03):int(H*0.30), int(W*0.68):int(W*0.97)]
        ch,cw=crop.shape[:2]; side=min(ch,cw); crop=crop[0:side,0:side]
        crop=cv2.resize(crop,(240,240),interpolation=cv2.INTER_LANCZOS4)
        cv2.imwrite(out_path, crop, [cv2.IMWRITE_JPEG_QUALITY, 92])
        return "FALLBACK"
    except Exception as e:
        return "ERROR:"+str(e)

pdfs = sorted([f for f in os.listdir(pdf_dir) if f.endswith('.pdf')])
pdfs = [f for f in pdfs if int(f.split('_')[0]) >= start_no]
ok=0; fb=0; err=0
for fname in pdfs:
    out_name = fname.replace('.pdf','.jpg')
    if os.path.exists(os.path.join(out_dir, out_name)):
        continue
    result = extract(os.path.join(pdf_dir,fname), os.path.join(out_dir,out_name))
    if "IMAGE" in result: ok+=1
    elif "FALLBACK" in result: fb+=1
    else: err+=1
    sys.stdout.buffer.write(("%s | %s\n"%(result,fname)).encode('utf-8'))
    sys.stdout.flush()
sys.stdout.buffer.write(("OK=%d FALLBACK=%d ERROR=%d\n"%(ok,fb,err)).encode('utf-8'))