import binascii
import magic
import argparse

def init_argparse():
    parser = argparse.ArgumentParser(prog="f1x_my_1m4g3",
                                     description="Fix corrupted images",
                                     epilog="https://github.com/barishaxxer/fix_your_image")
    parser.add_argument("-f","--file",help="Target image",nargs=1,required=True)
    parser.add_argument("-i", "--identify", help="Identify file type", required=False,action="store_true")
    return parser.parse_args()


def main():
    args = init_argparse()




def identify_file_type(file_path):
    with open("test.txt", "rb") as file:
        data = file.read()
        data_hex = binascii.hexlify(data).decode("utf-8")

    with open("test24.txt", "wb") as files:
        files.write(binascii.unhexlify(data_hex.replace("73","98")))



main()