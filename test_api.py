import fitz
print("version:", fitz.__version__)
doc = fitz.open(r"pdfs\001_Kyo Tagoo Naing.pdf")
page = doc[0]
images = page.get_images(full=True)
print("images:", len(images))
if images:
    xref = images[0][0]
    base = doc.extract_image(xref)
    print("keys:", list(base.keys()))
    print("size:", base["width"], "x", base["height"])
    print("ext:", base["ext"])
    # バイトデータをPixmapに
    img_bytes = base["image"]
    print("bytes len:", len(img_bytes))