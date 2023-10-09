# Hidden Message

>> Could you find the hidden message?

We are given an image and its name is `lsb.png`? Is it Least-Significant-Bit steganography? I don't think so =)). We have tried to use several tools online but it doesn't work lmao.

However, if you zoom in the upper left corner of the image, you may see some strange colored dots among white. With `Pillow`, you can have the value of the pixel:

```Python
from PIL import Image 

im = Image.open("lsb.png")
px = im.load()
print(px[0, 0])
```
Then the result is `(127, 255, 255, 255)`. The white color is `(255, 255, 255, 255)`. If you notice, `255 = 0b1111111` and `127 = 0b01111111`. So isn't it Most-Significant-Bit 😂. Actually, the flag (in ASCII bits & bytes) is hidden in the image by the rule:
+ If `i` bit is `0`, the pixel `[i, 0]` is flipped from `0b11111111` to `0b01111111`. 
+ Else, remains.

Then the solution is quite easy already. Flag: `ASCIS{w3ll_d0n3_st3g0_1s_fun}`
