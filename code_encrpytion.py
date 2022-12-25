#-*- coding:utf-8 -*-
import base64
import rsa
import os
from server import *
import tkinter.messagebox as msgbox
from Crypto.PublicKey import RSA



encrpyt_file_list = []
decrpyt_file_list = []
code_file_list = ['.py','.js','.cs','.ts']
code_file_list_2 = ['.php']


KEY_LENGTH = 1024

def GeneratePublicKey():
    with open('private.pem','r') as h:
        key = RSA.importKey(h.read())
    publickey = key.publickey()
    with open('public.pem','wb+') as f:
        f.write(publickey.exportKey('PEM'))


def GenerateAllKey():
    privatekey = RSA.generate(KEY_LENGTH)
    with open('private.pem','wb+') as f:
        f.write(privatekey.exportKey('PEM'))
    publickey = privatekey.publickey()
    with open('public.pem','wb+') as f:
        f.write(publickey.exportKey('PEM'))

def Check_Code():
    for (path,dir,files) in os.walk("."):
        for file in files:
            if file[-3:] in code_file_list:
                if file[-3:] == '.js':
                    file_type = "//"
                elif file[-3:] == '.py':
                    file_type = "#"
                with open(os.path.join(path,file),'rt', encoding='UTF8') as f:
                    text = f.readlines()
                if file_type+"encryption_underline\n" in text:
                    encrpyt_file_list.append(os.path.join(path,file))
                    

    


def Encrpytion(name,userid):
    Check_Code()
    edited_lines = []
    public_key_bytes = open('public.pem','rb').read()
    public_key = rsa.PublicKey.load_pkcs1_openssl_pem(keyfile=public_key_bytes)
    encrpyt_mode = False

    send_file_info = {
        "filename": name,
        "file_list": encrpyt_file_list
    }
    if GetFileInfo(send_file_info.get('filename'),userid) != None:
        if msgbox.askyesno("확인필요","이미 존재하는 이름입니다. 덮어씌웁니까?"):
            DeleteFileData(userid,send_file_info.get('filename'))
            UpdateFileData(userid,send_file_info)
        else:
            encrpyt_file_list.clear()
            return
    else:
        UpdateFileData(userid,send_file_info)
    for file_dir in encrpyt_file_list:
        with open(file_dir , 'rt', encoding='UTF8') as f:
            lines = f.readlines()
            if file_dir[-3:] == '.py':
                file_type = '#'
            elif file_dir[-3:] == '.js':
                file_type = '//'

            for line in lines:
                if line == file_type+'encryption_underline\n':
                    edited_lines.append(file_type+'encrypted\n')
                    encrpyt_mode = True
                    continue
                if encrpyt_mode == True:
                    line = line.encode('UTF8')
                    encrpyted_bytes = rsa.encrypt(line,public_key)
                    encrpyted_msg = base64.b64encode(encrpyted_bytes).decode('UTF-8')
                    edited_lines.append(encrpyted_msg+'\n')
                    encrpyt_mode = False
                else:
                    edited_lines.append(line)
        with open(file_dir,'wt', encoding='UTF8') as f:
            f.writelines(edited_lines)
        edited_lines.clear()
    msgbox.showinfo("알림","암호화가 완료되었습니다.")


    

def Decrpytion(name,userid):
    edited_lines = []
    private_key_bytes = open('private.pem','rb').read()
    private_key = rsa.PrivateKey.load_pkcs1(keyfile=private_key_bytes)
    decrpyt_mode = False
    decrpyt_file_list = GetFileInfo(name,userid)
    for file_dir in decrpyt_file_list:
        with open(file_dir, 'rt', encoding='UTF8') as f:
            lines = f.readlines()
            if file_dir[-3:] == '.py':
                file_type = '#'
            elif file_dir[-3:] == '.js':
                file_type = '//'

            for line in lines:
                if line == file_type+'encrypted\n':
                    edited_lines.append(file_type+'encryption_underline\n')
                    decrpyt_mode = True
                    continue
                if decrpyt_mode == True:
                    line = base64.b64decode(line)
                    line = rsa.decrypt(line,private_key).decode("UTF-8")
                    edited_lines.append(line)
                    decrpyt_mode = False
                else:
                    edited_lines.append(line)
                
        with open(file_dir,'wt', encoding='UTF8') as f:
            f.writelines(edited_lines)
        edited_lines.clear()
    msgbox.showinfo("알림","복호화가 완료되었습니다.")
