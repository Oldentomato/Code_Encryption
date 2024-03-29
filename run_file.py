#-*- coding:utf-8 -*-
import os
from tkinter import *
from tkinter import ttk
import tkinter.messagebox as msgbox
from werkzeug.security import generate_password_hash, check_password_hash
import code_encrpytion as enc
from server import *
import sys
#pyinstaller 로 인해 필요함
import base64
import rsa
import mongo_url as url
from pymongo import MongoClient
from Crypto.PublicKey import RSA


if getattr(sys, 'frozen', False):
    #test.exe로 실행한 경우,test.exe를 보관한 디렉토리의 full path를 취득
    program_directory = os.path.dirname(os.path.abspath(sys.executable))
else:
    #python test.py로 실행한 경우,test.py를 보관한 디렉토리의 full path를 취득
    program_directory = os.path.dirname(os.path.abspath(__file__))
#현재 작업 디렉토리를 변경
os.chdir(program_directory)

window = Tk()
window.geometry("500x200")
window.resizable(False,False)
window.title("Login")


frame_login = Frame(window)
frame_register = Frame(window)
frame_main = Frame(window)

frame_login.grid(row=0, column=0, sticky="nsew")
frame_register.grid(row=0, column=0, sticky="nsew")
frame_main.grid(row=0, column=0, sticky="nsew")

user_id , password = StringVar(), StringVar()
register_id, register_pass = StringVar(), StringVar()

en_file_name,de_file_name = StringVar(), StringVar()


def set_treeview():
    pass

def set_gitignore():
    write_mode = False
    with open('.gitignore','r') as f:
        line = f.readlines()
        if 'private.pem' or 'private.pem\n' not in line:
            write_mode = True
    if write_mode == True:
        with open('.gitignore','a+') as f:
            f.write('private.pem\n')

def openFrame(windowname,frame):
    window.title(windowname)
    frame.tkraise()

def upload_key(id):
    with open('private.pem','r') as f:
        pem = f.read()
    UpdateKeyData(id,pem)
    # os.system('rm -rf private.pem')

def download_key(id):
    if not os.path.isfile('public.pem') or not os.path.isfile('private.pem'):
        result = GetUserInfo(id)
        if result['private_key'] == "":
            msgbox.showinfo("알림","키파일이 조회되지 않아 새로 생성합니다.")
            enc.GenerateAllKey()
            upload_key(id)
        else:
            if not os.path.isfile('private.pem'): #private 이 없을 경우
                with open('private.pem','w') as f:
                    f.writelines(result['private_key'])
                msgbox.showinfo("확인","private key 생성됨")
            if not os.path.isfile('public.pem'): #public 이 없을 경우
                enc.GeneratePublicKey()
                msgbox.showinfo("확인","public key 생성됨")
        set_gitignore()
    else:
        msgbox.showinfo("알림","이미 키들을 가지고 있습니다.")
            

def login():
    last_signup = GetUserInfo(user_id.get())
    if last_signup == None:
        msgbox.showinfo("로그인 실패","해당 아이디는 조회되지 않음")
    elif check_password_hash(last_signup.get("password"),password.get()):
        #메인화면 페이지
        window.geometry("1000x500")
        window.title("Main")
        Label(frame_main, text = "Welcome " + user_id.get()).grid(row = 0, column = 1, padx = 10, pady = 10)
        Button(frame_main, text = 'Download_Key',command=lambda:[download_key(user_id.get())]).grid(row = 1, column = 1, padx = 10, pady = 10)
        Label(frame_main, text = "ProjectName: ").grid(row = 2, column = 1, padx = 10, pady = 10)
        Entry(frame_main, textvariable = en_file_name).grid(row = 2, column = 3, padx = 10, pady = 10)
        Button(frame_main, text = 'Encrpytion',command=lambda:[enc.Encrpytion(en_file_name.get(),user_id.get())]).grid(row = 4, column = 1, padx = 10, pady = 10)
        Label(frame_main, text = "ProjectName: ").grid(row = 5, column = 1, padx = 10, pady = 10)
        Entry(frame_main, textvariable = de_file_name).grid(row = 5, column = 3, padx = 10, pady = 10)
        Button(frame_main, text = 'Decrpytion',command=lambda:[enc.Decrpytion(de_file_name.get(),user_id.get())]).grid(row = 6, column = 1, padx = 10, pady = 10)
        Label(frame_main, text = "Projects ").grid(row = 0, column = 5, padx = 10, pady = 10)
        Button(frame_main, text = 'logout',command=lambda:[openFrame("login",frame_login)]).grid(row = 7, column = 1, padx = 10, pady = 10)

        files = GetAllFileInfo(user_id.get())

        tree = ttk.Treeview(frame_main)
        tree["columns"] = ("project name", "dirs")
        tree.column("project name",width=100)
        tree.column("dirs",width=300)
        tree.heading("#0",text="project name")
        tree.heading("#1",text="dirs")

        for index,file in enumerate(files):
            tree_id = tree.insert("","end","project"+str(index),text="Project : "+str(file['filename']))
            for dir in file['file_list']:
                dir = str(dir).replace("\\","/")
                tree.insert(tree_id, "end", text=" ", values=(dir))


        tree.grid(row = 1, column = 5, padx = 10, pady = 10)
        openFrame("main",frame_main)
    else:
        msgbox.showinfo("로그인 실패","비밀번호가 틀림")

def regist_userinfo():
    find_id = GetUserInfo(register_id.get())
    if find_id == None:
        if register_id.get() != "" and register_pass.get() != "":
            to_db = {
                "id": register_id.get(),
                "password": generate_password_hash(register_pass.get()),
                "private_key": "",
                "Files":[]
            }
            InsertInfo(to_db)
            msgbox.showinfo("회원가입","회원가입 성공")
            openFrame("login",frame_login)
        else:
            msgbox.showinfo("알림","아이디, 비밀번호를 모두 입력해주십시오")
    else:
        msgbox.showerror("알림","해당 아이디는 존재합니다")





#회원가입 페이지
Label(frame_register, text = "Username : ").grid(row = 0, column = 0, padx = 10, pady = 10)
Label(frame_register, text = "Password : ").grid(row = 1, column = 0, padx = 10, pady = 10)
Entry(frame_register, textvariable = register_id).grid(row = 0, column = 1, padx = 10, pady = 10)
Entry(frame_register, textvariable = register_pass, show='*').grid(row = 1, column = 1, padx = 10, pady = 10)
Button(frame_register, text = 'register',command=regist_userinfo).grid(row = 2, column = 1, padx = 10, pady = 10)
Button(frame_register, text = 'back',command=lambda:[openFrame("login",frame_login)]).grid(row = 2, column = 0, padx = 10, pady = 10)

#로그인 페이지
Label(frame_login, text = "Username : ").grid(row = 0, column = 0, padx = 10, pady = 10)
Label(frame_login, text = "Password : ").grid(row = 1, column = 0, padx = 10, pady = 10)
Entry(frame_login, textvariable = user_id).grid(row = 0, column = 1, padx = 10, pady = 10)
Entry(frame_login, textvariable = password, show='*').grid(row = 1, column = 1, padx = 10, pady = 10)
Button(frame_login, text = "Login", command = login).grid(row = 2, column = 0, padx = 15, pady = 10)
Button(frame_login, text = 'register',command=lambda:[openFrame("register",frame_register)]).grid(row = 2, column = 1, padx = 1, pady = 10)


openFrame("login",frame_login)
window.mainloop()

#pyinstaller --onefile run_file.py