import os
from pymongo import MongoClient
from tkinter import *
import tkinter.messagebox as msgbox
import mongo_url 
from werkzeug.security import generate_password_hash, check_password_hash


user_name = ''
client = MongoClient(host=mongo_url.url, port=27017)
db = client['crypto_db']
collection = db['user_info']
window = Tk()
window.geometry("500x200")
window.resizable(False,False)

frame_login = Frame(window)
frame_register = Frame(window)
frame_main = Frame(window)

frame_login.grid(row=0, column=0, sticky="nsew")
frame_register.grid(row=0, column=0, sticky="nsew")
frame_main.grid(row=0, column=0, sticky="nsew")

user_id , password = StringVar(), StringVar()
register_id, register_pass = StringVar(), StringVar()

def set_gitignore():
    print('test')

def openFrame(frame):
    frame.tkraise()

def upload_key(id):
    with open('private_pem','r') as f:
        pem = f.read()
    collection.update_one({"id":id},{"$set":{"private_key":pem}})
    # os.system('rm -rf private.pem')

def download_key(id):
    result = collection.find_one({"id":id})
    if result['private_key'] == "":
        msgbox.showinfo("알림","키파일이 조회되지 않아 새로 생성합니다.")
        os.system('openssl genrsa -out private.pem 4096') # generating private_key
        os.system('openssl rsa -in private.pem -out public.pem -pubout')# generating public_key
        set_gitignore()
        upload_key(id)
    else:
        with open('private_pem','w') as f:
            f.writelines(result['private_key'])
            


def login():
    last_signup = collection.find_one({"id":user_id.get()})
    if last_signup == None:
        msgbox.showinfo("로그인 실패","해당 아이디는 조회되지 않음")
    elif check_password_hash(last_signup.get("password"),password.get()):
        #메인화면 페이지
        Label(frame_main, text = "Welcome " + user_id.get()).grid(row = 0, column = 0, padx = 10, pady = 10)
        Button(frame_main, text = 'Download_Key',command=lambda:[download_key(user_id.get())]).grid(row = 1, column = 0, padx = 10, pady = 10)
        openFrame(frame_main)
    else:
        msgbox.showinfo("로그인 실패","비밀번호가 틀림")

def regist_userinfo():
    to_db = {
        "id": register_id.get(),
        "password": generate_password_hash(register_pass.get()),
        "private_key": ""
    }
    collection.insert_one(to_db)
    msgbox.showinfo("회원가입","회원가입 성공")
    openFrame(frame_login)



#회원가입 페이지
Entry(frame_register, textvariable = register_id).grid(row = 0, column = 1, padx = 10, pady = 10)
Entry(frame_register, textvariable = register_pass, show='*').grid(row = 1, column = 1, padx = 10, pady = 10)
Button(frame_register, text = 'register',command=regist_userinfo).grid(row = 2, column = 1, padx = 10, pady = 10)

#로그인 페이지
Label(frame_login, text = "Username : ").grid(row = 0, column = 0, padx = 10, pady = 10)
Label(frame_login, text = "Password : ").grid(row = 1, column = 0, padx = 10, pady = 10)
Entry(frame_login, textvariable = user_id).grid(row = 0, column = 1, padx = 10, pady = 10)
Entry(frame_login, textvariable = password, show='*').grid(row = 1, column = 1, padx = 10, pady = 10)
Button(frame_login, text = "Login", command = login).grid(row = 2, column = 1, padx = 10, pady = 10)
Button(frame_login, text = 'register',command=lambda:[openFrame(frame_register)]).grid(row = 2, column = 2, padx = 10, pady = 10)




openFrame(frame_login)
window.mainloop()