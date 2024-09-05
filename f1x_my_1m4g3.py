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
    if identify_file_type(args.file[0]) == "bmp":
        if args.identify:
            print("Identified file type as bmp")
            exit(0)
        print("Identified file type as bmp, fixing...")
        print(fix_bmp(args.file[0]))
    else :
        print("File type not supported")
        exit(1)




def fix_bmp(file_path):
    with open(file_path,"rb") as f:
        data = f.read()

        hex_data = binascii.hexlify(data).decode("utf-8")
        #fix magic byte
        fx_magic_byte = hex_data.replace(hex_data[:4],"424d",1)
        #next 4 bytes are file size
        le_1, le_2, le_3, le_4 = [hex_data[a:a+2] for a in [4, 6, 8, 10]]

        #because bmp files using little endian reverse
        file_size = int(le_4+le_3+le_2+le_1,16) - 54
        #fix DIB header
        fix_dib = fx_magic_byte.replace(fx_magic_byte[20:36],"3600000028000000",1)
        #width
        width1,width2,width3,width4 = [fix_dib[n:n+2] for n in range(36, 44, 2)]

        actual_width = int(width4+width3+width2+width1,16)
        #height
        height1,height2,height3,height4 = [fix_dib[i:i+2] for i in range(44, 52, 2)]
        actual_height = int(height4+height3+height2+height1,16)
        actual_size = actual_width * actual_height * 3
        if actual_size < file_size:
            if actual_height > actual_width:
                req_width = hex(file_size // (actual_height * 3))
                req_height = hex(actual_height)
            elif actual_width > actual_height:
                req_height = hex(file_size // (actual_width * 3))
                req_width = hex(actual_width)
        #fin_img = fix_dib.replace(fix_dib[])
        return req_width, req_height

def identify_file_type(file_path):
   mgc = magic.Magic()
   file_type = mgc.from_file(file_path)
   if file_type == "data":
       return "bmp"
   return file_type














main()