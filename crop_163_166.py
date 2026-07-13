import fitz, os

repoDir = r'C:\\Users\\NL－DG　PC1\\Desktop\\Work\\nldg-cv'
pdf_dir = os.path.join(repoDir, 'pdfs')
out_dir = os.path.join(repoDir, 'photos')
workspace = r'C:\\Users\\NL－DG　PC1\\AppData\\Roaming\\Genspark Claw\\users\\74ec096b-b6e9-452b-9a02-f93fbd1489de\\workspace'

# Vision AIによる位置情報を使って正確にクロップ
# (x0r, y0r, x1r, y1r) = ページ全体に対する割合
regions = {
    '163_Tin Moh Moh Oo.pdf':   (0.79, 0.08, 0.94, 0.22),
    '164_Pan Lae Lae Mon.pdf':  (0.75, 0.09, 0.88, 0.19),
    '165_Nay Hlaing Tun.pdf':   (0.69, 0.07, 0.84, 0.18),
    '166_Thein Htaik Soe.pdf':  (0.40, 0.10, 0.48, 0.23),  # 横向きページ中央上部
}

zoom = 4

for pdf_name, (x0r, y0r, x1r, y1r) in regions.items():
    pdf_path = os.path.join(pdf_dir, pdf_name)
    jpg_name = pdf_name.replace('.pdf', '.jpg')
    out_path = os.path.join(out_dir, jpg_name)
    ws_path  = os.path.join(workspace, f'crop_{jpg_name}')

    doc = fitz.open(pdf_path)
    page = doc[0]
    pw, ph = page.rect.width, page.rect.height

    clip = fitz.Rect(pw*x0r, ph*y0r, pw*x1r, ph*y1r)
    mat  = fitz.Matrix(zoom, zoom)
    pix  = page.get_pixmap(matrix=mat, clip=clip)
    pix.save(out_path)
    pix.save(ws_path)
    doc.close()

    print(f'OK {jpg_name}: {os.path.getsize(out_path)}B  ({clip})')
