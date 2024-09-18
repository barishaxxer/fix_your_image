import binascii
import magic
import argparse

RESET = "\033[0m"
YELLOW = "\033[33m"
CYAN = "\033[36m"
GREEN = "\033[32m"
RED = "\033[31m"

def init_argparse():
    parser = argparse.ArgumentParser(
        prog="f1x_my_1m4g3",
        description="Fix corrupted images",
        epilog="https://github.com/barishaxxer/fix_your_image",
    )
    parser.add_argument("-f", "--file", help="Target image", nargs=1, required=True)
    parser.add_argument(
        "-i",
        "--identify",
        help="Identify file type",
        required=False,
        action="store_true",
    )
    return parser.parse_args()

def main():
    args = init_argparse()
    file_type = identify_file_type(args.file[0]).strip()

    if file_type in ["bmp", "png", "jpg", "gif"]:
        if args.identify:
            print(f"{GREEN}Identified file type as {file_type}{RESET}")
            exit(0)
        print(f"{YELLOW}Identified file type as {file_type}, fixing...{RESET}")
        if file_type == "bmp":
            print(fix_bmp(args.file[0]))
        elif file_type == "png":
            print(fix_png(args.file[0]))
        elif file_type == "jpg":
            print(fix_jpg(args.file[0]))
        elif file_type == "gif":
            print(fix_gif(args.file[0]))
    else:
        print("File type not supported")
        exit(1)

def fix_bmp(file_path):
    fx_magic_byte, fix_dib, file_size, actual_size, actual_height, actual_width = load_bmp(file_path)
    if file_size == actual_size:
        exit("No need to fix")
    print(fix_bmp_width(fix_dib, fx_magic_byte, file_size, actual_height))
    print(fix_bmp_height(fix_dib, fx_magic_byte, file_size, actual_width))
    print(fix_bmp_16_9(fix_dib, fx_magic_byte, file_size))
    return f"{GREEN}BMP image fixed successfully.{RESET}"

def fix_png(file_path):
    fx_magic_byte, fix_ihdr, file_size, actual_size, actual_height, actual_width = load_png(file_path)
    if file_size == actual_size:
        exit("No need to fix")
    print(fix_png_width(fix_ihdr, fx_magic_byte, file_size, actual_height))
    print(fix_png_height(fix_ihdr, fx_magic_byte, file_size, actual_width))
    print(fix_png_16_9(fix_ihdr, fx_magic_byte, file_size))
    return f"{GREEN}PNG image fixed successfully.{RESET}"

def fix_jpg(file_path):
    fx_magic_byte, fix_sof, file_size, actual_size, actual_height, actual_width = load_jpg(file_path)
    if file_size == actual_size:
        exit("No need to fix")
    print(fix_jpg_width(fix_sof, fx_magic_byte, file_size, actual_height))
    print(fix_jpg_height(fix_sof, fx_magic_byte, file_size, actual_width))
    print(fix_jpg_16_9(fix_sof, fx_magic_byte, file_size))
    return f"{GREEN}JPG image fixed successfully.{RESET}"

def fix_gif(file_path):
    fx_magic_byte, fix_lsd, file_size, actual_size, actual_height, actual_width = load_gif(file_path)
    if file_size == actual_size:
        exit("No need to fix")
    print(fix_gif_width(fix_lsd, fx_magic_byte, file_size, actual_height))
    print(fix_gif_height(fix_lsd, fx_magic_byte, file_size, actual_width))
    print(fix_gif_16_9(fix_lsd, fx_magic_byte, file_size))
    return f"{GREEN}GIF image fixed successfully.{RESET}"

# BMP fixing functions
def fix_bmp_width(fix_dib, fx_magic_byte, file_size, actual_height):
    if actual_height == 0:
        return f"{RED}Height is 0 passing this step{RESET}"
    req_width = hex(file_size // (actual_height * 3)).replace("0x", "").zfill(8)
    r2 = "".join([req_width[i : i + 2] for i in range(0, 8, 2)][::-1])
    fix = fx_magic_byte.replace(fix_dib[36:44], r2, 1)
    dib_fix = fix_dib.replace(fix_dib[36:44], r2, 1)
    with open("width.bmp", "wb") as y:
        y.write(binascii.unhexlify(fix))
    with open("offset_dib_width.bmp", "wb") as x:
        x.write(binascii.unhexlify(dib_fix))
    return f"{CYAN}Fixing: Fixed width will be saved as width.bmp suffix{RESET}"

def fix_bmp_height(fix_dib, fx_magic_byte, file_size, actual_width):
    if actual_width == 0:
        return f"{RED}Width is 0 passing this step{RESET}"
    req_height = hex(file_size // (actual_width * 3)).replace("0x", "").zfill(8)
    r1 = "".join([req_height[i : i + 2] for i in range(0, 8, 2)][::-1])
    fix = fx_magic_byte.replace(fix_dib[44:52], r1, 1)
    dib_fix = fix_dib.replace(fix_dib[44:52], r1, 1)
    with open("height.bmp", "wb") as z:
        z.write(binascii.unhexlify(fix))
    with open("offset_dib_height.bmp", "wb") as f:
        f.write(binascii.unhexlify(dib_fix))
    return f"{CYAN}Fixing: Fixed height will be saved as height.bmp suffix{RESET}"

def fix_bmp_16_9(fix_dib, fx_magic_byte, file_size):
    x = file_size // (16 * 3 * 9)
    x = x ** (1 / 2)
    heix = round(16 * x)
    widx = round(9 * x)
    width = hex(heix + (heix % 4)).replace("0x", "").zfill(8)
    height = hex(widx + (widx % 4)).replace("0x", "").zfill(8)
    r1 = "".join([height[i : i + 2] for i in range(0, 8, 2)][::-1])
    r2 = "".join([width[i : i + 2] for i in range(0, 8, 2)][::-1])
    fix = fx_magic_byte.replace(fix_dib[36:44], r2, 1)
    fix = fix.replace(fix[44:52], r1, 1)
    dib_fix = fix_dib.replace(fix_dib[36:44], r2, 1)
    dib_fix = dib_fix.replace(dib_fix[44:52], r1, 1)
    with open("16_9.bmp", "wb") as b:
        b.write(binascii.unhexlify(fix))
    with open("offset_dib_16_9.bmp", "wb") as a:
        a.write(binascii.unhexlify(dib_fix))
    return f"{CYAN}Fixing: Fixed 16:9 ratio will be saved as 16_9.bmp suffix{RESET}"

# PNG fixing functions
def fix_png_width(fix_ihdr, fx_magic_byte, file_size, actual_height):
    if actual_height == 0:
        return f"{RED}Height is 0 passing this step{RESET}"
    req_width = hex(file_size // (actual_height * 3)).replace("0x", "").zfill(8)
    fix = fx_magic_byte.replace(fix_ihdr[16:24], req_width, 1)
    ihdr_fix = fix_ihdr.replace(fix_ihdr[16:24], req_width, 1)
    with open("width.png", "wb") as y:
        y.write(binascii.unhexlify(fix))
    with open("offset_ihdr_width.png", "wb") as x:
        x.write(binascii.unhexlify(ihdr_fix))
    return f"{CYAN}Fixing: Fixed width will be saved as width.png suffix{RESET}"

def fix_png_height(fix_ihdr, fx_magic_byte, file_size, actual_width):
    if actual_width == 0:
        return f"{RED}Width is 0 passing this step{RESET}"
    req_height = hex(file_size // (actual_width * 3)).replace("0x", "").zfill(8)
    fix = fx_magic_byte.replace(fix_ihdr[24:32], req_height, 1)
    ihdr_fix = fix_ihdr.replace(fix_ihdr[24:32], req_height, 1)
    with open("height.png", "wb") as z:
        z.write(binascii.unhexlify(fix))
    with open("offset_ihdr_height.png", "wb") as f:
        f.write(binascii.unhexlify(ihdr_fix))
    return f"{CYAN}Fixing: Fixed height will be saved as height.png suffix{RESET}"

def fix_png_16_9(fix_ihdr, fx_magic_byte, file_size):
    x = file_size // (16 * 3 * 9)
    x = x ** (1 / 2)
    heix = round(16 * x)
    widx = round(9 * x)
    width = hex(heix).replace("0x", "").zfill(8)
    height = hex(widx).replace("0x", "").zfill(8)
    fix = fx_magic_byte.replace(fix_ihdr[16:24], width, 1)
    fix = fix.replace(fix[24:32], height, 1)
    ihdr_fix = fix_ihdr.replace(fix_ihdr[16:24], width, 1)
    ihdr_fix = ihdr_fix.replace(ihdr_fix[24:32], height, 1)
    with open("16_9.png", "wb") as b:
        b.write(binascii.unhexlify(fix))
    with open("offset_ihdr_16_9.png", "wb") as a:
        a.write(binascii.unhexlify(ihdr_fix))
    return f"{CYAN}Fixing: Fixed 16:9 ratio will be saved as 16_9.png suffix{RESET}"

# JPG fixing functions
def fix_jpg_width(fix_sof, fx_magic_byte, file_size, actual_height):
    if actual_height == 0:
        return f"{RED}Height is 0 passing this step{RESET}"
    req_width = hex(file_size // (actual_height * 3)).replace("0x", "").zfill(4)
    fix = fx_magic_byte.replace(fix_sof[10:14], req_width, 1)
    sof_fix = fix_sof.replace(fix_sof[10:14], req_width, 1)
    with open("width.jpg", "wb") as y:
        y.write(binascii.unhexlify(fix))
    with open("offset_sof_width.jpg", "wb") as x:
        x.write(binascii.unhexlify(sof_fix))
    return f"{CYAN}Fixing: Fixed width will be saved as width.jpg suffix{RESET}"

def fix_jpg_height(fix_sof, fx_magic_byte, file_size, actual_width):
    if actual_width == 0:
        return f"{RED}Width is 0 passing this step{RESET}"
    req_height = hex(file_size // (actual_width * 3)).replace("0x", "").zfill(4)
    fix = fx_magic_byte.replace(fix_sof[14:18], req_height, 1)
    sof_fix = fix_sof.replace(fix_sof[14:18], req_height, 1)
    with open("height.jpg", "wb") as z:
        z.write(binascii.unhexlify(fix))
    with open("offset_sof_height.jpg", "wb") as f:
        f.write(binascii.unhexlify(sof_fix))
    return f"{CYAN}Fixing: Fixed height will be saved as height.jpg suffix{RESET}"

def fix_jpg_16_9(fix_sof, fx_magic_byte, file_size):
    x = file_size // (16 * 3 * 9)
    x = x ** (1 / 2)
    heix = round(16 * x)
    widx = round(9 * x)
    width = hex(heix).replace("0x", "").zfill(4)
    height = hex(widx).replace("0x", "").zfill(4)
    fix = fx_magic_byte.replace(fix_sof[10:14], width, 1)
    fix = fix.replace(fix[14:18], height, 1)
    sof_fix = fix_sof.replace(fix_sof[10:14], width, 1)
    sof_fix = sof_fix.replace(sof_fix[14:18], height, 1)
    with open("16_9.jpg", "wb") as b:
        b.write(binascii.unhexlify(fix))
    with open("offset_sof_16_9.jpg", "wb") as a:
        a.write(binascii.unhexlify(sof_fix))
    return f"{CYAN}Fixing: Fixed 16:9 ratio will be saved as 16_9.jpg suffix{RESET}"

# GIF fixing functions
def fix_gif_width(fix_lsd, fx_magic_byte, file_size, actual_height):
    if actual_height == 0:
        return f"{RED}Height is 0 passing this step{RESET}"
    req_width = hex(file_size // (actual_height * 3)).replace("0x", "").zfill(4)
    r2 = "".join([req_width[i : i + 2] for i in range(0, 4, 2)][::-1])
    fix = fx_magic_byte.replace(fix_lsd[12:16],r2, 1)
    lsd_fix = fix_lsd.replace(fix_lsd[12:16], r2, 1)
    with open("width.gif", "wb") as y:
        y.write(binascii.unhexlify(fix))
    with open("offset_lsd_width.gif", "wb") as x:
        x.write(binascii.unhexlify(lsd_fix))
    return f"{CYAN}Fixing: Fixed width will be saved as width.gif suffix{RESET}"

def fix_gif_height(fix_lsd, fx_magic_byte, file_size, actual_width):
    if actual_width == 0:
        return f"{RED}Width is 0 passing this step{RESET}"
    req_height = hex(file_size // (actual_width * 3)).replace("0x", "").zfill(4)
    r1 = "".join([req_height[i : i + 2] for i in range(0, 4, 2)][::-1])
    fix = fx_magic_byte.replace(fix_lsd[16:20], r1, 1)
    lsd_fix = fix_lsd.replace(fix_lsd[16:20], r1, 1)
    with open("height.gif", "wb") as z:
        z.write(binascii.unhexlify(fix))
    with open("offset_lsd_height.gif", "wb") as f:
        f.write(binascii.unhexlify(lsd_fix))
    return f"{CYAN}Fixing: Fixed height will be saved as height.gif suffix{RESET}"

def fix_gif_16_9(fix_lsd, fx_magic_byte, file_size):
    x = file_size // (16 * 3 * 9)
    x = x ** (1 / 2)
    heix = round(16 * x)
    widx = round(9 * x)
    width = hex(heix).replace("0x", "").zfill(4)
    height = hex(widx).replace("0x", "").zfill(4)
    r1 = "".join([height[i : i + 2] for i in range(0, 4, 2)][::-1])
    r2 = "".join([width[i : i + 2] for i in range(0, 4, 2)][::-1])
    fix = fx_magic_byte.replace(fix_lsd[12:16], r2, 1)
    fix = fix.replace(fix[16:20], r1, 1)
    lsd_fix = fix_lsd.replace(fix_lsd[12:16], r2, 1)
    lsd_fix = lsd_fix.replace(lsd_fix[16:20], r1, 1)
    with open("16_9.gif", "wb") as b:
        b.write(binascii.unhexlify(fix))
    with open("offset_lsd_16_9.gif", "wb") as a:
        a.write(binascii.unhexlify(lsd_fix))
    return f"{CYAN}Fixing: Fixed 16:9 ratio will be saved as 16_9.gif suffix{RESET}"

def load_bmp(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
        hex_data = binascii.hexlify(data).decode("utf-8")
        fx_magic_byte = hex_data.replace(hex_data[:4], "424d", 1)
        le_1, le_2, le_3, le_4 = [hex_data[a : a + 2] for a in [4, 6, 8, 10]]
        file_size = int(le_4 + le_3 + le_2 + le_1, 16) - 54
        fix_dib = fx_magic_byte.replace(fx_magic_byte[20:36], "3600000028000000", 1)
        width1, width2, width3, width4 = [fix_dib[n : n + 2] for n in range(36, 44, 2)]
        actual_width = int(width4 + width3 + width2 + width1, 16)
        height1, height2, height3, height4 = [fix_dib[i : i + 2] for i in range(44, 52, 2)]
        actual_height = int(height4 + height3 + height2 + height1, 16)
        actual_size = actual_width * actual_height * 3
        return fx_magic_byte, fix_dib, file_size, actual_size, actual_height, actual_width

def load_png(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
        hex_data = binascii.hexlify(data).decode("utf-8")
        fx_magic_byte = hex_data.replace(hex_data[:16], "89504e470d0a1a0a", 1)
        ihdr_start = hex_data.find("49484452")
        fix_ihdr = fx_magic_byte[ihdr_start:ihdr_start+52]
        file_size = len(data) - 8
        width = int(fix_ihdr[16:24], 16)
        height = int(fix_ihdr[24:32], 16)
        actual_size = width * height * 3
        return fx_magic_byte, fix_ihdr, file_size, actual_size, height, width

def load_jpg(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
        hex_data = binascii.hexlify(data).decode("utf-8")
        fx_magic_byte = hex_data.replace(hex_data[:4], "ffd8", 1)
        sof_start = hex_data.find("ffc0")
        fix_sof = fx_magic_byte[sof_start:sof_start+36]
        file_size = len(data) - 2
        height = int(fix_sof[10:14], 16)
        width = int(fix_sof[14:18], 16)
        actual_size = width * height * 3
        return fx_magic_byte, fix_sof, file_size, actual_size, height, width

def load_gif(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
        hex_data = binascii.hexlify(data).decode("utf-8")
        fx_magic_byte = hex_data.replace(hex_data[:12], "474946383961", 1)
        fix_lsd = fx_magic_byte[12:26]
        file_size = len(data) - 6
        width1, width2 = fix_lsd[0:2], fix_lsd[2:4]
        width = int(width2 + width1, 16)
        height1, height2 = fix_lsd[4:6], fix_lsd[6:8]
        height = int(height2 + height1, 16)
        actual_size = width * height * 3
        return fx_magic_byte, fix_lsd, file_size, actual_size, height, width

def identify_file_type(file_path):
    mgc = magic.Magic()
    file_type = mgc.from_file(file_path)
    if file_type.strip() == "data" or file_type.startswith("PC bitmap"):
        return "bmp"
    elif file_type.startswith("PNG image data"):
        return "png"
    elif file_type.startswith("JPEG image data"):
        return "jpg"
    elif file_type.startswith("GIF image data"):
        return "gif"
    return file_type

if __name__ == "__main__":
    main()