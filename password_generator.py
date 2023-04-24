"""Generate HASH and SALT from CSV file."""
import os
import csv
import argparse
import hashlib
import binascii
import tqdm

# import random
# import string
# def generate_secret_code(): 
#     print(''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k=12)))

SECRET_CODE = "arCIqmZ$DgosU_"

def usage():
    print("Usage:")
    print("python3 password_generator.py -i <input_file> -o <output_file>")
    print("-i : Provide input file path.")
    print("-o : Provide output file path. (optional)")

def read_csv(filename):
    file_data = []
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            file_data.append(row)
        csvfile.close()
    
    return file_data


def generate_passwords_hash_salt(input_file, output_file):
    if os.path.isfile(input_file):
        try:
            with open(input_file, 'rb') as f:
                contents = f.read()
                f.close()
            contents = contents.replace(b'\x00', b'')
        except Exception as err:
            print(f"Error: Input CSV file {input_file} not found.")
            usage()
            exit(-1)

        try:
            temp_file = input_file + ".tmp"
            with open(temp_file, 'wb') as t:
                t.write(contents)
                t.close()
        except Exception as err:
            print("Error: Temporary file not found.")
            exit(-1)

        if os.path.isfile(temp_file):
            file_data = read_csv(temp_file)
            os.remove(temp_file)
        else:
            print("Error: Temporary file not found.")
            exit(-1)

        if len(output_file) == 0:
            output_dir = os.path.dirname(os.path.abspath(input_file))
            output_file = os.path.join(output_dir, "output.csv")
        
        if os.path.isfile(output_file):
            os.remove(output_file)
        
        print("Output File:", output_file)
        if not file_data:
            print(f"Error: Empty input CSV file: {input_file}")
            exit(-1)
        else:
            try:
                with open(output_file, mode='a', newline='') as o:
                    fields = ['passwords', "salt", "hash"]
                    writer = csv.writer(o)
                    writer.writerow(fields)
                    total_rows = len(file_data)
                    for i in tqdm.tqdm(range(total_rows), desc="Progress"):
                        if i != 0:
                            row = file_data[i]
                            count = 0
                            output_row = []
                            for cell in row:
                                if count == 5 and len(cell) != 0:
                                    salt = os.urandom(32)
                                    hashed = hashlib.pbkdf2_hmac("sha256", SECRET_CODE.encode("utf-8"), salt, 100000)
                                    output_row.append(cell)
                                    output_row.append(binascii.hexlify(salt))
                                    output_row.append(binascii.hexlify(hashed))
                                # if count == 5 and len(cell) == 0:
                                #     output_rows.append(cell)
                                #     output_rows.append("")

                                # output_data.append(output_row)
                                count = count + 1
                            writer.writerow(output_row)
                    o.close()
            except Exception as err:
                print(f"Error: Output CSV file {output_file} not found.")
                exit(-1)
    else:
        print(f"Error: Input CSV file {input_file} not found.")
        usage()
        exit(-1)


def parse_arguments():
    parser = argparse.ArgumentParser(description="Password Generator")
    parser.add_argument('-i', type=str, help="Path of Input CSV file.")
    parser.add_argument('-o', type=str, help="Path of Output CSV file.")
    args = parser.parse_args()

    return args


if __name__ == "__main__":
    input_file = ""
    output_file = ""
    args = parse_arguments()

    if args.i is not None:
        input_file = str(args.i)
        print("Input File:", input_file)
    
    if args.o is not None:
        output_file = str(args.o)
        
    generate_passwords_hash_salt(input_file, output_file)
