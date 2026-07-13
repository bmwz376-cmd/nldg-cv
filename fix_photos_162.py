import fitz, os

repoDir = r'C:\\Users\\NL－DG　PC1\\Desktop\\Work\\nldg-cv'
pdf_dir = os.path.join(repoDir, 'pdfs')
out_dir = os.path.join(repoDir, 'photos')

targets = [
    ('162_Thi Ha Soe.pdf', '162_Thi Ha Soe.jpg'),
    ('163_Tin Moh Moh Oo.pdf', '163_Tin Moh Moh Oo.jpg'),
    ('164_Pan Lae Lae Mon.pdf', '164_Pan Lae Lae Mon.jpg'),
    ('165_Nay Hlaing Tun.pdf', '165_Nay Hlaing Tun.jpg'),
    ('166_Thein Htaik Soe.pdf', '166_Thein Htaik Soe.jpg'),
]

for pdf_name, jpg_name in targets:
    pdf_path = os.path.join(pdf_dir, pdf_name)
    out_path = os.path.join(out_dir, jpg_name)
    size = os.path.getsize(out_path) if os.path.exists(out_path) else 0
    if size < 15000:
        print(f'Regenerating ({size}B): {jpg_name}')
        doc = fitz.open(pdf_path)
        page = doc[0]
        clip = fitz.Rect(0, 0, page.rect.width * 0.45, page.rect.height * 0.38)
        pix = page.get_pixmap(matrix=fitz.Matrix(2,2), clip=clip)
        pix.save(out_path)
        doc.close()
        print(f'  -> {os.path.getsize(out_path)} bytes')
    else:
        print(f'OK ({size}B): {jpg_name}')
