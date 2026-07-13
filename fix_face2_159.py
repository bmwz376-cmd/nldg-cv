import fitz, os

repoDir = r'C:\\Users\\NL－DG　PC1\\Desktop\\Work\\nldg-cv'
pdf_dir = os.path.join(repoDir, 'pdfs')
out_dir = os.path.join(repoDir, 'photos')
workspace = r'C:\\Users\\NL－DG　PC1\\AppData\\Roaming\\Genspark Claw\\users\\74ec096b-b6e9-452b-9a02-f93fbd1489de\\workspace'

# 今度は顔写真枠のみ（文字が入らないよう縮小）
# 159: x=0.79-0.91, y=0.09-0.19
# 160: x=0.74-0.87, y=0.09-0.19  
# 161: x=0.73-0.85, y=0.12-0.22
face_regions = {
    '159_Lae Yi Win.pdf':       (0.79, 0.09, 0.91, 0.19),
    '160_Thuzar Myint.pdf':     (0.74, 0.09, 0.87, 0.19),
    '161_Aye Thandar Aung.pdf': (0.73, 0.12, 0.85, 0.22),
}

zoom = 4

for pdf_name, (x0r, y0r, x1r, y1r) in face_regions.items():
    pdf_path = os.path.join(pdf_dir, pdf_name)
    jpg_name = pdf_name.replace('.pdf', '.jpg')
    out_path = os.path.join(out_dir, jpg_name)

    doc = fitz.open(pdf_path)
    page = doc[0]
    pw, ph = page.rect.width, page.rect.height

    clip = fitz.Rect(pw*x0r, ph*y0r, pw*x1r, ph*y1r)
    mat = fitz.Matrix(zoom, zoom)
    pix = page.get_pixmap(matrix=mat, clip=clip)
    pix.save(out_path)
    
    # workspace確認用
    ws_path = os.path.join(workspace, f'face2_{pdf_name.split("_")[0]}.jpg')
    pix.save(ws_path)
    
    doc.close()
    sz = os.path.getsize(out_path)
    print(f'OK {jpg_name}: {sz}B')
