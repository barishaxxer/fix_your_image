import binascii
import magic
import argparse


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

    if identify_file_type(args.file[0]).strip() == "bmp":
        if args.identify:
            print("Identified file type as bmp")
            exit(0)
        print("Identified file type as bmp, fixing...")
        print(fix_bmp(args.file[0]))
    else:
        print("File type not supported")
        exit(1)


def fix_bmp(file_path):
    fx_magic_byte, fix_dib, file_size, actual_size, actual_height, actual_width = (
        load_bmp(file_path)
    )
    if file_size == actual_size:
        exit("No need to fix")
    print(fix_bmp_width(file_path, fix_dib, fx_magic_byte, file_size, actual_height))
    print(fix_bmp_height(file_path, fix_dib, fx_magic_byte, file_size, actual_width))
    print(fix_bmp_16_9(file_path, fix_dib, fx_magic_byte, file_size))
    return "Fixed images saved as width.bmp and height.bmp"


def fix_bmp_width(file_path, fix_dib, fx_magic_byte, file_size, actual_height):
    """
    Keeps the height and fixes the width of the image to reach the actual size
    :param file_path:
    :param fix_dib:
    :param fx_magic_byte:
    :param file_size:
    :param actual_height:
    :return: String

    """
    if actual_height == 0:
        return "Height is 0 passing this step"
    req_width = hex(file_size // (actual_height * 3)).replace("0x", "").zfill(8)
    r2 = "".join([req_width[i : i + 2] for i in range(0, 8, 2)][::-1])
    fix = fx_magic_byte.replace(fix_dib[36:44], r2, 1)
    dib_fix = fix_dib.replace(fix_dib[36:44], r2, 1)
    with open("width.bmp", "wb") as y:
        y.write(binascii.unhexlify(fix))
    with open("offset_dib_width.bmp", "wb") as x:
        x.write(binascii.unhexlify(dib_fix))
    return "Fixed width saved as width.bmp suffix"


def fix_bmp_height(file_path, fix_dib, fx_magic_byte, file_size, actual_width):
    """
    Keeps the width and fixes the width of the image to reach the actual size
    :param file_path:
    :param fix_dib:
    :param fx_magic_byte:
    :param file_size:
    :param actual_width:
    :return: String

    """
    if actual_width == 0:
        return "Width is 0 passing this step"
    req_height = hex(file_size // (actual_width * 3)).replace("0x", "").zfill(8)

    r1 = "".join([req_height[i : i + 2] for i in range(0, 8, 2)][::-1])

    fix = fx_magic_byte.replace(fix_dib[44:52], r1, 1)
    dib_fix = fix_dib.replace(fix_dib[44:52], r1, 1)
    with open("height.bmp", "wb") as z:
        z.write(binascii.unhexlify(fix))
    with open("offset_dib_height.bmp", "wb") as f:
        f.write(binascii.unhexlify(dib_fix))
    return "Fixed height saved as height.bmp suffix"


def load_bmp(file_path):
    with open(file_path, "rb") as f:
        data = f.read()

        hex_data = binascii.hexlify(data).decode("utf-8")
        # fix magic byte
        fx_magic_byte = hex_data.replace(hex_data[:4], "424d", 1)
        # next 4 bytes are file size
        le_1, le_2, le_3, le_4 = [hex_data[a : a + 2] for a in [4, 6, 8, 10]]

        # because bmp files using little endian reverse
        file_size = int(le_4 + le_3 + le_2 + le_1, 16) - 54

        # fix DIB header
        fix_dib = fx_magic_byte.replace(fx_magic_byte[20:36], "3600000028000000", 1)
        # width
        width1, width2, width3, width4 = [fix_dib[n : n + 2] for n in range(36, 44, 2)]

        actual_width = int(width4 + width3 + width2 + width1, 16)
        # height
        height1, height2, height3, height4 = [
            fix_dib[i : i + 2] for i in range(44, 52, 2)
        ]
        actual_height = int(height4 + height3 + height2 + height1, 16)
        actual_size = actual_width * actual_height * 3
        return (
            fx_magic_byte,
            fix_dib,
            file_size,
            actual_size,
            actual_height,
            actual_width,
        )


def fix_bmp_16_9(file_path, fix_dib, fx_magic_byte, file_size):
    # according to 16:9 aspect ratio
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

    return "Fixed 16:9 ratio saved as 16_9.bmp suffix"


def identify_file_type(file_path):
    mgc = magic.Magic()
    file_type = mgc.from_file(file_path)
    if file_type.strip() == "data" or file_type.startswith("PC bitmap"):
        return "bmp"
    return file_type


main()
