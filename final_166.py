import fitz, os

repoDir = r'C:\\Users\\NL－DG　PC1\\Desktop\\Work\\nldg-cv'
pdf_dir = os.path.join(repoDir, 'pdfs')
out_dir = os.path.join(repoDir, 'photos')
workspace = r'C:\\Users\\NL－DG　PC1\\AppData\\Roaming\\Genspark Claw\\users\\74ec096b-b6e9-452b-9a02-f93fbd1489de\\workspace'

# 166: 上下余白を減らす（y0を大きく、y1を小さく）
pdf166 = os.path.join(pdf_dir, '166_Thein Htaik Soe.pdf')
doc = fitz.open(pdf166)
page = doc[0]
pw, ph = page.rect.width, page.rect.height

# 前回y0=0.100 y1=0.205 → 余白除去: y0=0.112 y1=0.194
clip = fitz.Rect(pw*0.414, ph*0.112, pw*0.471, ph*0.194)
pix = page.get_pixmap(matrix=fitz.Matrix(8, 8), clip=clip)
out = os.path.join(out_dir, '166_Thein Htaik Soe.jpg')
pix.save(out)
pix.save(os.path.join(workspace, 'crop5_166.jpg'))
doc.close()
print(f'166 final: {os.path.getsize(out)}B  pix={pix.width}x{pix.height}')
