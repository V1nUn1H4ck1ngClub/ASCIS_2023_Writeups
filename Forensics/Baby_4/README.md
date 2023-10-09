# Baby_4

#forensics #minidump 

In this challenge, we are given a minidump file. 

![](images/Pasted%20image%2020231009074306.png)

Let's see which type of dump is that:

![](images/Pasted%20image%2020231009074350.png)

With these information, I started to search the web and it talked about open WinDbg. So I tried too :D.

![](images/Pasted%20image%2020231009074641.png)

So from what we see here, it is a dump from CobaltStrike attack, and the error code is a breakpoint has been reached? This is the first time I played a Forensics challenge (in a true way :)), so I can't do anything else. I have tried to apply `string` command to the dump file but it does not work. And indeedly, we haven't got the challenge during competition time. 

After the competition, I have a little bit research on this. I tried to be a script kiddie by installing `Volatility` and indeed, I can't do anything but cry T.T 

![](images/Pasted%20image%2020231009080039.png)

However, after the competition, thanks to my old intern friends in VCS from team `KMA.NOT2BAD` - #1 in Northern Bracket (kudos to you guys too), I got some hints of the challenge .

# IDA dump the PE 
So, with IDA Pro, you can open dump file too. Let's do it first. Also, remember to open it with IDA64. 

![](images/Pasted%20image%2020231009075217.png)

From the modules, you can see the CobaltStrike.exe here, with base is `0x46000` and offset is `0x7000`. You can save the memory region with single IDAPython command:

```Python
idc.savefile("Path to dump", 0, 0x46000, 0x7000)
```
However, remember to format the slash as `C:\\Users\\b1b1RE\\Desktop\\Samples\\dumps_test.bin`, else you can't dump the binary. Now you got the dump version of this only CobaltStrike region. 
You can use a tool called [PE_Dump_Fixer](https://github.com/skadro-official/PE-Dump-Fixer) to fix the dump into a PE file. The usage is really simple, I will not cover it here. 
# IDA do some reversing :D 
After you got the PE from the dump, you can open with IDA to get it reverse the binary for you. However, in this part, you need IDA x86 to open it. But before doing that, why don't we run the binary first? 

![](images/Pasted%20image%2020231009080538.png)

=))

Okay, let's reverse it. 

## Analysis
![](images/Pasted%20image%2020231009081229.png)

So basically, in normal case, the program will automatically quit and prompt the "Opps" MessageBox. You can forge the conditional jump but it is not what we consider here. If you can jump out the conditional, then the program will format the [`BCRYPT_KEY_DATA_BLOB`](https://learn.microsoft.com/en-us/windows/win32/api/bcrypt/ns-bcrypt-bcrypt_key_data_blob_header) object (as it is required in the `BCryptImportKey`, whereas in my case, the blob is the variable `v4`). The layout of the object:

```Cpp
typedef struct _BCRYPT_KEY_DATA_BLOB_HEADER {
  ULONG dwMagic;
  ULONG dwVersion;
  ULONG cbKeyData;
} BCRYPT_KEY_DATA_BLOB_HEADER, *PBCRYPT_KEY_DATA_BLOB_HEADER;
```

The first `dwMagic` must hold the value as char `MBDK`. At first I was to dump to realize that I need to bruce-force the 4 characters =))). Shame on me. After the format of blob key, the program will decrypt a memory in `ciphertext` as I renamed in AES CBC mode of operation, but it is not what we care in this scenario. 

Let's run the program without the `Opps` :)

![](images/Pasted%20image%2020231009081427.png)

Damn :). However, if you look at the line from `32` to `34`, actually, the key was XORed a little bit. What if we tried to decrypt the data without the XOR? Indeed there is a way is you can remove the XOR part :))))

![](images/Pasted%20image%2020231009082452.png)

Gotcha! But I used a Python script to decrypt manually so let's count it here :)

So first, you need to get the ciphertext. 
![](images/Pasted%20image%2020231009081918.png)

You can do this IDAPython command for it:

```Python
list(idaapi.get_bytes(0x4643F8, 0x40))
```
where `0x4643F8` is address of ciphertext and `0x40` is it size. These information you can get in the function [`BCryptDecrypt`](https://learn.microsoft.com/en-us/windows/win32/api/bcrypt/nf-bcrypt-bcryptdecrypt). You also need the original key too. For this I just copy it. 

![](images/Pasted%20image%2020231009081856.png)
Also, the size for this `key` is 16 bytes, exact the size of AES key. 

Next, you can put in Python with supports of `pycryptodome` to have the decrypt works for you. 

```Python
from Crypto.Util.number import *
from Crypto.Cipher import AES

# ciphertext from IDA
ciphertext = [0x21, 0x57, 0x99, 0x4c, 0xde, 0x82, 0x72, 0x94, 0x8f, 0x6b, 0xd, 0xaf, 0xa6, 0x83, 0xcb, 0xa3, 0xb6, 0xbb, 0x5e, 0x9e, 0xca, 0xf9, 0x42, 0xe7, 0x47, 0x9c, 0xb7, 0x6, 0xb0, 0x1a, 0xd2, 0xc3, 0x7b, 0xb7, 0xcb, 0xcf, 0x96, 0xc3, 0x97, 0xb9, 0x65, 0xd5, 0x35, 0xfc, 0x2c, 0x2, 0xcc, 0x70, 0x4e, 0x7a, 0xc2, 0x37, 0x1, 0x45, 0xa1, 0xa2, 0x2f, 0x4c, 0xfc, 0xaa, 0x3e, 0x3e, 0x9f, 0x99]

# convert list to bytes
ciphertext = bytes(ciphertext)
pbBinary = 0x8CBBE5F15134EEF7B5297BD92BA76B01
pb = long_to_bytes(pbBinary)

# reformat to little endianess
pb = list(pb)[::-1]
pb = bytes(pb)

# Decrypt :)
AES_ECB = AES.new(pb, AES.MODE_ECB)
plaintext = AES_ECB.decrypt(ciphertext)
print(plaintext)
```

Flag: `ASCIS{H4v3_Y0u_7ri3d_u5ing_57RINg5_0N_M3M0RY_dUmp}`
