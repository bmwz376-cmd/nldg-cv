import fitz, os

repoDir = r'C:\\Users\\NL－DG　PC1\\Desktop\\Work\\nldg-cv'
pdf_dir = os.path.join(repoDir, 'pdfs')
workspace = r'C:\\Users\\NL－DG　PC1\\AppData\\Roaming\\Genspark Claw\\users\\74ec096b-b6e9-452b-9a02-f93fbd1489de\\workspace'

# 各PDFから顔写真候補を抽出してworkspaceに保存
extracts = [
    (163, 'Tin Moh Moh Oo', 0, 1),   # p0 img[1] = 217x290
    (164, 'Pan Lae Lae Mon', 0, 0),   # p0 img[0] = 207x248
    (165, 'Nay Hlaing Tun',  0, 0),   # p0 img[0] = 236x264
    (166, 'Thein Htaik Soe', 0, 0),   # p0 img[0] = 133x156
]

for no, name, pno, img_idx in extracts:
    pdf_path = os.path.join(pdf_dir, f'{no}_{name}.pdf')
    doc = fitz.open(pdf_path)
    xref = doc[pno].get_images(full=True)[img_idx][0]
    base = doc.extract_image(xref)
    out = os.path.join(workspace, f'embed_{no}.{base["ext"]}')
    with open(out, 'wb') as f: f.write(base['image'])
    print(f'{no}_{name}: {base["width"]}x{base["height"]} {os.path.getsize(out)}B -> {out}')
    doc.close()
