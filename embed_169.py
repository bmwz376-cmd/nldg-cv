import fitz, os

repoDir = r'C:\\Users\\NL－DG　PC1\\Desktop\\Work\\nldg-cv'
pdf_path = os.path.join(repoDir, 'pdfs', '169_Phyo Hein Kyaw.pdf')
out_path = os.path.join(repoDir, 'photos', '169_Phyo Hein Kyaw.jpg')
ws_path  = os.path.join(r'C:\\Users\\NL－DG　PC1\\AppData\\Roaming\\Genspark Claw\\users\\74ec096b-b6e9-452b-9a02-f93fbd1489de\\workspace', 'embed_169.jpg')

# 埋め込みJPEGを直接抽出（225x286px）
doc = fitz.open(pdf_path)
xref = doc[0].get_images(full=True)[0][0]
base = doc.extract_image(xref)
with open(out_path, 'wb') as f: f.write(base['image'])
with open(ws_path,  'wb') as f: f.write(base['image'])
doc.close()
print(f'embed: {base["width"]}x{base["height"]} {os.path.getsize(out_path)}B ext={base["ext"]}')
