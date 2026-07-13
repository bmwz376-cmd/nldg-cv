import fitz, os
doc = fitz.open(r'C:\\Users\\NL－DG　PC1\\Desktop\\Work\\02_人材紹介_CV・履歴書\\ワールド候補2名\\ye cv form(1).pdf')
page = doc[0]
text = page.get_text()[:500]
print('=== ye cv form テキスト ===')
print(text)
# プレビュー
pix = page.get_pixmap(matrix=fitz.Matrix(1.5, 1.5))
pix.save(r'C:\\Users\\NL－DG　PC1\\AppData\\Roaming\\Genspark Claw\\users\\74ec096b-b6e9-452b-9a02-f93fbd1489de\\workspace\prev_ye.png')
doc.close()
