import fitz, os

pdf_path = os.path.join(r'C:\\Users\\NL－DG　PC1\\Desktop\\Work\\nldg-cv', 'pdfs', '162_Thi Ha Soe.pdf')
out_path = os.path.join(r'C:\\Users\\NL－DG　PC1\\Desktop\\Work\\nldg-cv', 'photos', '162_Thi Ha Soe.jpg')

doc = fitz.open(pdf_path)
xref = doc[0].get_images(full=True)[0][0]
base = doc.extract_image(xref)
with open(out_path, 'wb') as f: f.write(base['image'])
doc.close()
print(f'saved: {os.path.getsize(out_path)}B  {base["width"]}x{base["height"]}')
