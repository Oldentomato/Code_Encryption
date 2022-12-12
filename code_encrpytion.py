import base64
import rsa
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('--dir', type=str, help='set file directory', required=True)

args = parser.parse_args()

edited_lines = []
public_key_bytes = open('public.pem','rb').read()
public_key = rsa.PublicKey.load_pkcs1_openssl_pem(keyfile=public_key_bytes)
encrpyt_mode = False


with open(args.dir) as f:
    lines = f.readlines()
    for index,line in enumerate(lines):
        if line == '#encrpytion_underline\n':
            edited_lines.append('#encrpyted\n')
            encrpyt_mode = True
            continue
        if encrpyt_mode == True:
            line = line.encode('utf-8')
            encrpyted_bytes = rsa.encrypt(line,public_key)
            encrpyted_msg = base64.b64encode(encrpyted_bytes).decode('utf-8')
            edited_lines.append(encrpyted_msg+'\n')
            encrpyt_mode = False
        else:
            edited_lines.append(line)
with open('test_code.py','w') as f:
    f.writelines(edited_lines)
