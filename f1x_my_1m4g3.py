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
    if identify_file_type(args.file[0]) == "bmp":
        print("Identified file type as bmp")
        fix_bmp(args.file[0])
    else:
        print("File type not supported")
        exit(1)


def identify_file_type(file_path):
    mgc = magic.Magic()
    file_type = mgc.from_file(file_path)
    if file_type == "data":
        return "bmp"
    return file_type


main()
