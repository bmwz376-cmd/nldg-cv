import fitz, os

repoDir = r'C:\\Users\\NL－DG　PC1\\Desktop\\Work\\nldg-cv'
pdf_dir = os.path.join(repoDir, 'pdfs')
out_dir = os.path.join(repoDir, 'photos')

for no, name in [(159, 'Lae Yi Win'), (160, 'Thuzar Myint'), (161, 'Aye Thandar Aung')]:
    pdf_path = os.path.join(pdf_dir, f'{no}_{name}.pdf')
    doc = fitz.open(pdf_path)
    page = doc[0]
    # 全ページを低解像度でプレビュー出力（確認用）
    pix = page.get_pixmap(matrix=fitz.Matrix(1.5, 1.5))
    preview_path = os.path.join(out_dir, f'preview_{no}.png')
    pix.save(preview_path)
    print(f'{no}_{name}: page size={page.rect.width:.0f}x{page.rect.height:.0f}, preview={os.path.getsize(preview_path)}B -> {preview_path}')
    doc.close()
