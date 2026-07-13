import fitz, os

repoDir = r'C:\\Users\\NL－DG　PC1\\Desktop\\Work\\nldg-cv'
pdf_dir = os.path.join(repoDir, 'pdfs')
out_dir = os.path.join(repoDir, 'photos')

# 各PDFの顔写真位置（画像分析結果）
face_regions = {
    '159_Lae Yi Win.pdf':       (0.79, 0.09, 0.12, 0.12),  # (x_start, y_start, w_ratio, h_ratio)
    '160_Thuzar Myint.pdf':     (0.74, 0.09, 0.13, 0.12),
    '161_Aye Thandar Aung.pdf': (0.73, 0.12, 0.12, 0.12),
}

zoom = 4  # 高解像度

for pdf_name, (xr, yr, wr, hr) in face_regions.items():
    pdf_path = os.path.join(pdf_dir, pdf_name)
    jpg_name = pdf_name.replace('.pdf', '.jpg')
    out_path = os.path.join(out_dir, jpg_name)

    doc = fitz.open(pdf_path)
    page = doc[0]
    pw, ph = page.rect.width, page.rect.height

    # マージンを少し広げて確実に顔を含める
    x0 = pw * (xr - 0.01)
    y0 = ph * (yr - 0.01)
    x1 = pw * (xr + wr + 0.02)
    y1 = ph * (yr + hr + 0.02)
    clip = fitz.Rect(x0, y0, x1, y1)

    mat = fitz.Matrix(zoom, zoom)
    pix = page.get_pixmap(matrix=mat, clip=clip)
    pix.save(out_path)
    doc.close()

    sz = os.path.getsize(out_path)
    print(f'OK {jpg_name}: {sz}B  clip=({x0:.0f},{y0:.0f},{x1:.0f},{y1:.0f})')
