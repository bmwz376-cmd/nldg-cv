import fitz, os

repoDir = r'C:\\Users\\NL－DG　PC1\\Desktop\\Work\\nldg-cv'
pdf_dir = os.path.join(repoDir, 'pdfs')
out_dir = os.path.join(repoDir, 'photos')
workspace = r'C:\\Users\\NL－DG　PC1\\AppData\\Roaming\\Genspark Claw\\users\\74ec096b-b6e9-452b-9a02-f93fbd1489de\\workspace'
zoom = 4

# 163: 右端縦線を除くためx1を0.92に縮小
pdf163 = os.path.join(pdf_dir, '163_Tin Moh Moh Oo.pdf')
doc = fitz.open(pdf163)
page = doc[0]
pw, ph = page.rect.width, page.rect.height
clip = fitz.Rect(pw*0.793, ph*0.082, pw*0.920, ph*0.215)
pix = page.get_pixmap(matrix=fitz.Matrix(zoom,zoom), clip=clip)
out = os.path.join(out_dir, '163_Tin Moh Moh Oo.jpg')
pix.save(out)
pix.save(os.path.join(workspace, 'final_163.jpg'))
doc.close()
print(f'163 final: {os.path.getsize(out)}B')
