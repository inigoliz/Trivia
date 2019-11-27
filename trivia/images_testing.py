from PIL import Image
from time import time
import pytesseract as pys  # OCR

t0 = time()
im = Image.open("../samples/spain_1/sample_trivia_1.jpeg")

box_q = (130, 410, 950, 1040)
q = im.crop(box_q)
box_r1 = (210, 1280, 900, 1340)
r1 = im.crop(box_r1)
box_r2 = (210, 1465, 900, 1525)
r2 = im.crop(box_r2)
box_r3 = (210, 1650, 900, 1710)
r3 = im.crop(box_r3)

Q = pys.image_to_string(q, lang='eng')
R1 = pys.image_to_string(r1, lang='eng')
R2 = pys.image_to_string(r2, lang='eng')
R3 = pys.image_to_string(r3, lang='eng')

print(f'elapsed time {time()-t0}')

print(im.format, im.size, im.mode)
print(Q)
print(R1, R2, R3)

im.show()
