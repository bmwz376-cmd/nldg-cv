import fitz, os

repoDir = r'C:\\Users\\NL－DG　PC1\\Desktop\\Work\\nldg-cv'
pdf_dir = os.path.join(repoDir, 'pdfs')
workspace = r'C:\\Users\\NL－DG　PC1\\AppData\\Roaming\\Genspark Claw\\users\\74ec096b-b6e9-452b-9a02-f93fbd1489de\\workspace'

# 164: ページ上部1/3を高解像度で出力
doc164 = fitz.open(os.path.join(pdf_dir, '164_Pan Lae Lae Mon.pdf'))
page = doc164[0]
pw, ph = page.rect.width, page.rect.height
# 上部40%を拡大表示
clip = fitz.Rect(0, 0, pw, ph*0.4)
pix = page.get_pixmap(matrix=fitz.Matrix(2.5, 2.5), clip=clip)
pix.save(os.path.join(workspace, 'zoom_164_top.png'))
print(f'164 page: {pw:.0f}x{ph:.0f}')
doc164.close()

# 166: ページ上部1/3を高解像度で出力  
doc166 = fitz.open(os.path.join(pdf_dir, '166_Thein Htaik Soe.pdf'))
page = doc166[0]
pw, ph = page.rect.width, page.rect.height
clip = fitz.Rect(0, 0, pw, ph*0.5)
pix = page.get_pixmap(matrix=fitz.Matrix(2.5, 2.5), clip=clip)
pix.save(os.path.join(workspace, 'zoom_166_top.png'))
print(f'166 page: {pw:.0f}x{ph:.0f}')
doc166.close()
