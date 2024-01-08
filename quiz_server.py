import socket
from threading import Thread
import random

server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
ip_address="127.0.0.1"
port=8000

server.bind((ip_address,port))
server.listen()

list_of_clients=[]
nicknames=[]
print("Server has started.")

questions=[
    "Who is the author of Harry Potter? \n a.Lucas Flint\n b.JK Rowling\n c.Thomas Mann\n d.William Shakespeare",
    "Which is the largest state in India? \n a.Rajasthan\n b.Madhya Pradesh\n c.Uttar Pradesh\n d.Maharashtra"
]

answers=[
    "b",
    "a"
]

def remove(con):
    if con in list_of_clients:
        list_of_clients.remove(con)
    
def get_random_question_answer(con):
    random_index=random.randint(0,len(questions)-1)
    random_question=questions[random_index]
    random_answer=answers[random_index]
    con.send(random_question.encode("utf-8"))
    return random_index,random_question,random_answer

def remove_question(index):
    questions.pop(index)
    answers.pop(index)

def client_thread(con,adr):
    score=0
    con.send("WELCOME TO THE QUIZ GAME".encode("utf-8"))
    con.send("You will receive a question.The answer to the question should be one of a,b,c or d\n".encode("utf-8"))
    con.send("Good Luck!\n\n".encode("utf-8"))
    index,question,answer=get_random_question_answer(con)

    while True:
        try:
            message=con.recv(2048).decode("utf-8")
            if message:
                if message.split(":")[-1].lower()==answer:
                    score+=1
                    con.send(f"Bravo! Your score is {score}\n\n".encode("utf-8"))
                else:
                    con.send("Incorrect answer! Better luck next time\n\n".encode("utf-8"))
                remove_question(index)
                index,question,answer=get_random_question_answer(con)
            else:
                remove(con)
        except:
            continue



while True:
    con,adr=server.accept()
    con.send("NICKNAME".encode("utf-8"))
    nickname=con.recv(2048).decode("utf-8")
    list_of_clients.append(con)
    nicknames.append(nickname)
    print(nickname +" connected!")
    new_thread=Thread(target=client_thread,args=(con,adr))
    new_thread.start()