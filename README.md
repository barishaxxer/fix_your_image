# Fix Corrupted Images
Save your corrupted images easily.A powerful image forensic tool.
This repository comes with a ctf challenge to showcase tools usage purposes(0xByteStream_Challenge_Corrupted_File) and its restored version(Example_Fixed_Image.bmp).
<details>
  <summary>Ctf solution</summary>
```bash
python f1x_my_1m4g3.py -f 0xByteStream_Challenge_Corrupted_File
```

</details>
## Usage
İdentify Mode:
```bash
python f1x_my_1m4g3.py -i -f 0xByteStream_Challenge_Corrupted_File
```
Fix Image:
```bash
python f1x_my_1m4g3.py -f 0xByteStream_Challenge_Corrupted_File
```
## How it works
Manipulates image bytes to fix.Works under three mode:
1. 16:9 Aspect Ratio
2. Steady width, fill size with increasing height
3. Steady height, fill size with increasing width

# **TO DO**
-[x] BMP file fix
-[] JPG file fix
-[] PNG file fix
-[] PDF file fix
-[] GIF file fix

# Collaborate
Check CONTRIBUTING.md

