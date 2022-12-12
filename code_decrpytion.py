import base64
import rsa
import os
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('--dir', type=str, help='set file directory', required=True)

args = parser.parse_args()


edited_lines = []
private_key_bytes = open('private.pem','rb').read()
private_key = rsa.PrivateKey.load_pkcs1(keyfile=private_key_bytes)
decrpyt_mode = False


with open(args.dir) as f:
    lines = f.readlines()
    for index,line in enumerate(lines):
        if line == '#encrpyted\n':
            edited_lines.append('#encrpytion_underline\n')
            decrpyt_mode = True
            continue
        if decrpyt_mode == True:
            line = base64.b64decode(line)
            line = rsa.decrypt(line,private_key).decode('utf-8')
            edited_lines.append(line)
            decrpyt_mode = False
        else:
            edited_lines.append(line)
with open('test_code.py','w') as f:
    f.writelines(edited_lines)
