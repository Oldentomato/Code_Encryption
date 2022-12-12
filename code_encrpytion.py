import base64
import rsa


def Encrpytion(dir):
    edited_lines = []
    public_key_bytes = open('public.pem','rb').read()
    public_key = rsa.PublicKey.load_pkcs1_openssl_pem(keyfile=public_key_bytes)
    encrpyt_mode = False

    with open('test_code.py') as f:
        lines = f.readlines()
        for line in lines:
            if line == '#encrpytion_underline\n':
                edited_lines.append('#encrpyted\n')
                encrpyt_mode = True
                continue
            if encrpyt_mode == True:
                line = line.encode('utf-8')
                encrpyted_bytes = rsa.encrypt(line,public_key)
                encrpyted_msg = base64.b64encode(encrpyted_bytes).decode('utf-8')
                edited_lines.append('#'+encrpyted_msg+'\n')
                encrpyt_mode = False
            else:
                edited_lines.append(line)
    with open('test_code.py','w') as f:
        f.writelines(edited_lines)

def Decrpytion(dir):
    edited_lines = []
    private_key_bytes = open('private.pem','rb').read()
    private_key = rsa.PrivateKey.load_pkcs1(keyfile=private_key_bytes)
    decrpyt_mode = False

    with open('test_code.py') as f:
        lines = f.readlines()
        for line in lines:
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
