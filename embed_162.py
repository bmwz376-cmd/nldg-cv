import fitz, os

repoDir = r'C:\\Users\\NL－DG　PC1\\Desktop\\Work\\nldg-cv'
workspace = r'C:\\Users\\NL－DG　PC1\\AppData\\Roaming\\Genspark Claw\\users\\74ec096b-b6e9-452b-9a02-f93fbd1489de\\workspace'
pdf_path = os.path.join(repoDir, 'pdfs', '162_Thi Ha Soe.pdf')
out_path = os.path.join(repoDir, 'photos', '162_Thi Ha Soe.jpg')
ws_path  = os.path.join(workspace, 'check_162_embed.jpg')

# まず埋め込みJPEGを直接抽出して確認
doc = fitz.open(pdf_path)
xref = doc[0].get_images(full=True)[0][0]
base = doc.extract_image(xref)
with open(ws_path, 'wb') as f: f.write(base['image'])
print(f'embed: {base["width"]}x{base["height"]} {len(base["image"])}B ext={base["ext"]}')
doc.close()
