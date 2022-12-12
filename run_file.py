import os
from pymongo import MongoClient
from tkinter import *
import mongo_url as url
import tkinter.messagebox as msgbox
from werkzeug.security import generate_password_hash, check_password_hash
import code_encrpytion as enc

client = MongoClient(host=url.url, port=27017)
db = client['crypto_db']
collection = db['user_info']
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

file_path = StringVar()

def set_gitignore():
    with open('.gitignore','a+') as f:
        line = f.readlines()
        if '\nprivate.pem' or 'private.pem' or 'private.pem\n' not in line:
            f.write('\nprivate.pem')

def openFrame(frame):
    frame.tkraise()

def upload_key(id):
    with open('private.pem','r') as f:
        pem = f.read()
    collection.update_one({"id":id},{"$set":{"private_key":pem}})
    # os.system('rm -rf private.pem')

def download_key(id):
    if not os.path.isfile('public.pem') or not os.path.isfile('private.pem'):
        result = collection.find_one({"id":id})
        if result['private_key'] == "":
            msgbox.showinfo("알림","키파일이 조회되지 않아 새로 생성합니다.")
            os.system('openssl genrsa -out private.pem 4096') # generating private_key
            os.system('openssl rsa -in private.pem -out public.pem -pubout')# generating public_key
            upload_key(id)
        else:
            if not os.path.isfile('private.pem'):
                with open('private.pem','w') as f:
                    f.writelines(result['private_key'])
            if not os.path.isfile('public.pem'):
                os.system('openssl rsa -in private.pem -out public.pem -pubout')
        set_gitignore()
    else:
        msgbox.showinfo("알림","이미 키들을 가지고 있습니다.")
            


def login():
    last_signup = collection.find_one({"id":user_id.get()})
    if last_signup == None:
        msgbox.showinfo("로그인 실패","해당 아이디는 조회되지 않음")
    elif check_password_hash(last_signup.get("password"),password.get()):
        #메인화면 페이지
        window.geometry("500x500")
        window.title("Main")
        Label(frame_main, text = "Welcome " + user_id.get()).grid(row = 0, column = 3, padx = 10, pady = 10)
        Button(frame_main, text = 'Download_Key',command=lambda:[download_key(user_id.get())]).grid(row = 1, column = 3, padx = 10, pady = 10)
        Button(frame_main, text = 'Encrpytion',command=lambda:[enc.Encrpytion(file_path.get())]).grid(row = 3, column = 3, padx = 10, pady = 10)
        Button(frame_main, text = 'Decrpytion',command=lambda:[enc.Decrpytion(file_path.get())]).grid(row = 4, column = 3, padx = 10, pady = 10)
        openFrame(frame_main)
    else:
        msgbox.showinfo("로그인 실패","비밀번호가 틀림")

def regist_userinfo():
    find_id = collection.find_one({"id":register_id.get()})
    if find_id == None:
        if register_id.get() != "" and register_pass.get() != "":
            to_db = {
                "id": register_id.get(),
                "password": generate_password_hash(register_pass.get()),
                "private_key": ""
            }
            collection.insert_one(to_db)
            msgbox.showinfo("회원가입","회원가입 성공")
            openFrame(frame_login)
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

#로그인 페이지
Label(frame_login, text = "Username : ").grid(row = 0, column = 0, padx = 10, pady = 10)
Label(frame_login, text = "Password : ").grid(row = 1, column = 0, padx = 10, pady = 10)
Entry(frame_login, textvariable = user_id).grid(row = 0, column = 1, padx = 10, pady = 10)
Entry(frame_login, textvariable = password, show='*').grid(row = 1, column = 1, padx = 10, pady = 10)
Button(frame_login, text = "Login", command = login).grid(row = 2, column = 0, padx = 15, pady = 10)
Button(frame_login, text = 'register',command=lambda:[openFrame(frame_register)]).grid(row = 2, column = 1, padx = 1, pady = 10)


openFrame(frame_login)
window.mainloop()