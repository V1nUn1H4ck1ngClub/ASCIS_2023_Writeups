from PIL import Image 

im = Image.open("lsb.png")
px = im.load()

res = []
for i in range(0, 729):
    if px[i, 0] == (127, 255, 255, 255):
        res.append("0")
    else:
        res.append("1")
print(res)

for i in range(0, 729, 8):
    print(chr(int("".join(res[i:i+8]), 2)), end="")