import socket
from threading import Thread
from tkinter import *

# nickname=input("Choose your nickname : ")
client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

ip_address="127.0.0.1"
port=8000

client.connect((ip_address,port))

print("Connected with the server.")

class GUI:
    def __init__(self):
        self.window=Tk()
        self.window.withdraw()

        self.login=Toplevel()
        self.login.title("Login")
        self.login.resizable(width=False,height=False)
        self.login.configure(width=400,height=400)

        self.heading=Label(self.login,text="Please login to continue",justify=CENTER,font="Helvetica 14 bold")
        self.heading.place(relheight=0.15,relx=0.2,rely=0.07)

        self.labelName=Label(self.login,text="Name : ",font="Helvetica 12")
        self.labelName.place(relheight=0.2,relx=0.1,rely=0.2)

        self.entryName=Entry(self.login,font="Helvetica 14")
        self.entryName.place(relwidth=0.4,relheight=0.12,relx=0.35,rely=0.25)
        self.entryName.focus()

        self.go=Button(self.login,text="CONTINUE",font="Helvetica 14 bold",command=lambda: self.goAhead(self.entryName.get()))
        self.go.place(relx=0.4,rely=0.55)


        self.window.mainloop()

    def goAhead(self,name):
        self.login.destroy()
        #self.name=name
        self.layout(name)
        rcv=Thread(target=self.receive)
        rcv.start()

    def receive(self):
        while True:
            try:
                message=client.recv(2048).decode("utf-8")
                if message=="NICKNAME":
                    client.send(self.name.encode("utf-8"))
                else:
                    pass
            except:
                print("An error occured.")
                client.close()
                break

    def layout(self,name):
        self.name=name
        self.window.deiconify()
        self.window.title("CHATROOM")
        self.window.resizable(width=False,height=False)
        self.window.configure(width=470,height=550,bg="#17202a")

        self.labelHead=Label(self.window,text=self.name,bg="#17202a",fg="#eaecee",font="Helvetica 13 bold",pady=5)
        self.labelHead.place(relwidth=1)

        self.line=Label(self.window,width=450,bg="#abb2b9")
        self.line.place(relwidth=1,rely=0.07,relheight=0.012)

        self.textBox=Text(self.window,width=20,height=2,bg="#17202a",fg="#eaecee",font="Helvetica 14",padx=5,pady=5)
        self.textBox.place(relheight=0.745,relwidth=1,rely=0.08)

        self.labelBottom=Label(self.window,bg="#abb2b9",height=80)
        self.labelBottom.place(relwidth=1,rely=0.825)
        
        self.inputBox=Entry(self.labelBottom,bg="#2c3e50",fg="#eaecee",font="Helvetica 13")
        self.inputBox.place(relwidth=0.74,relheight=0.06,rely=0.008,relx=0.011)
        self.inputBox.focus()

        self.button=Button(self.labelBottom,text="SEND",font="Helvetica 10 bold",width=20,bg="#abb2b9",command=lambda: self.sendMessage(self.inputBox.get()))
        self.button.place(relx=0.77,rely=0.008,relheight=0.06,relwidth=0.22)

        self.textBox.config(cursor="arrow")

        scrollbar=Scrollbar(self.textBox)
        scrollbar.place(relheight=1,relx=0.974)
        scrollbar.config(command=self.textBox.yview)

        self.textBox.config(state=DISABLED)

    def sendMessage(self,msg):
        self.textBox.config(state=DISABLED)
        self.message=msg
        self.inputBox.delete(0,END)
        sendMsg=Thread(target=self.write)
        sendMsg.start()

    def showMessage(self,msg):
        self.textBox.config(state=NORMAL)
        self.textBox.insert(END,msg+"\n\n")
        self.textBox.config(state=DISABLED)
        self.textBox.see(END)

    def write(self):
        self.textBox.config(state=DISABLED)
        while True:
            message=(f"{self.name}:{self.message}")
            client.send(message.encode("utf-8"))
            self.showMessage(message)
            break

    def receive(self):
        while True:
            try:
                message=client.recv(2048).decode("utf-8")
                if message=="NICKNAME":
                    client.send(self.name.encode("utf-8"))
                else:
                    self.showMessage(message)
            except:
                print("An error occured.")
                client.close()
                break

g=GUI()