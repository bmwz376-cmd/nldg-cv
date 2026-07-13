import fitz, os

repoDir = r'C:\\Users\\NL－DG　PC1\\Desktop\\Work\\nldg-cv'
pdf_dir = os.path.join(repoDir, 'pdfs')
out_dir = os.path.join(repoDir, 'photos')

# 160と161も念のためページレンダリング版で確認（サイズが小さすぎる場合）
targets = [
    ('159_Lae Yi Win.pdf', '159_Lae Yi Win.jpg'),
    ('160_Thuzar Myint.pdf', '160_Thuzar Myint.jpg'),
    ('161_Aye Thandar Aung.pdf', '161_Aye Thandar Aung.jpg'),
]

for pdf_name, jpg_name in targets:
    pdf_path = os.path.join(pdf_dir, pdf_name)
    out_path = os.path.join(out_dir, jpg_name)
    
    if os.path.exists(out_path):
        size = os.path.getsize(out_path)
        if size < 15000:  # 15KB未満は再生成
            print(f'Regenerating (too small {size}B): {jpg_name}')
            doc = fitz.open(pdf_path)
            page = doc[0]
            mat = fitz.Matrix(2, 2)
            # ページ上部左側の顔写真エリア
            clip = fitz.Rect(0, 0, page.rect.width * 0.4, page.rect.height * 0.38)
            pix = page.get_pixmap(matrix=mat, clip=clip)
            pix.save(out_path)
            doc.close()
            print(f'  -> Saved: {os.path.getsize(out_path)} bytes')
        else:
            print(f'OK ({size}B): {jpg_name}')

print('Done.')
