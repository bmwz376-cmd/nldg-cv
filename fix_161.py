import fitz, os

repoDir = r'C:\\Users\\NL－DG　PC1\\Desktop\\Work\\nldg-cv'
pdf_dir = os.path.join(repoDir, 'pdfs')
out_dir = os.path.join(repoDir, 'photos')
workspace = r'C:\\Users\\NL－DG　PC1\\AppData\\Roaming\\Genspark Claw\\users\\74ec096b-b6e9-452b-9a02-f93fbd1489de\\workspace'

zoom = 4

# 161: 右端の枠線を避けるため x1を小さくする
pdf_path = os.path.join(pdf_dir, '161_Aye Thandar Aung.pdf')
doc = fitz.open(pdf_path)
page = doc[0]
pw, ph = page.rect.width, page.rect.height

# x0を少し右、x1を少し左に調整（枠線を除去）
clip = fitz.Rect(pw*0.745, ph*0.12, pw*0.835, ph*0.22)
mat = fitz.Matrix(zoom, zoom)
pix = page.get_pixmap(matrix=mat, clip=clip)

out_path = os.path.join(out_dir, '161_Aye Thandar Aung.jpg')
pix.save(out_path)
ws_path = os.path.join(workspace, 'face3_161.jpg')
pix.save(ws_path)
doc.close()
print(f'OK 161: {os.path.getsize(out_path)}B')
