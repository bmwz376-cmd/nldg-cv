import fitz, os

repoDir = r'C:\\Users\\NL－DG　PC1\\Desktop\\Work\\nldg-cv'
pdf_dir = os.path.join(repoDir, 'pdfs')
out_dir = os.path.join(repoDir, 'photos')
workspace = r'C:\\Users\\NL－DG　PC1\\AppData\\Roaming\\Genspark Claw\\users\\74ec096b-b6e9-452b-9a02-f93fbd1489de\\workspace'
zoom = 4

# 164: x0=0.724 y0=0.088 x1=0.854 y1=0.196 (元PDF 595x842)
pdf164 = os.path.join(pdf_dir, '164_Pan Lae Lae Mon.pdf')
doc = fitz.open(pdf164)
page = doc[0]
pw, ph = page.rect.width, page.rect.height
clip = fitz.Rect(pw*0.724, ph*0.088, pw*0.854, ph*0.196)
pix = page.get_pixmap(matrix=fitz.Matrix(zoom,zoom), clip=clip)
out = os.path.join(out_dir, '164_Pan Lae Lae Mon.jpg')
pix.save(out)
pix.save(os.path.join(workspace, 'crop2_164.jpg'))
doc.close()
print(f'164: {os.path.getsize(out)}B  clip={clip}')

# 166: x0=0.407 y0=0.096 x1=0.485 y1=0.220 (元PDF 792x612)
pdf166 = os.path.join(pdf_dir, '166_Thein Htaik Soe.pdf')
doc = fitz.open(pdf166)
page = doc[0]
pw, ph = page.rect.width, page.rect.height
clip = fitz.Rect(pw*0.407, ph*0.096, pw*0.485, ph*0.220)
pix = page.get_pixmap(matrix=fitz.Matrix(zoom,zoom), clip=clip)
out = os.path.join(out_dir, '166_Thein Htaik Soe.jpg')
pix.save(out)
pix.save(os.path.join(workspace, 'crop2_166.jpg'))
doc.close()
print(f'166: {os.path.getsize(out)}B  clip={clip}')
