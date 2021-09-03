from tkinter import *
from tkinter.messagebox import showinfo
import socket

import os
import sys

def readHoF():
    global hofPlayer
    global txthof
    
    try:
        hof = open('HallOfFame.txt','r')
    except IOError:
        print("Error : Cannot find file or read data")    
    else:
        for i in hof:
              name, play, win, lose, draw = i.split(':')
              hofPlayer.update({str(name):[int(play), int(win), int(lose), int(draw)]})  
        hof.close()
    i = 0
    for key, value in sorted(hofPlayer.items(), key=lambda r: r[1][1], reverse=True):
        i += 1
#----------------------------------ADD DRAW--------------------------------------------#
        string = '  '+str(i)+"  - "+str(key)+'\t\t: '+str(hofPlayer[key][0])+' : '+str(hofPlayer[key][1])+' : '+str(hofPlayer[key][2])+' : '+str(hofPlayer[key][3])+'\n'
#----------------------------------ADD DRAW--------------------------------------------#  
        txthof.insert(END, string + '\n')
        
def writeHoF():
    try:
        new = open(r'HallOfFame.txt', 'w', encoding = 'utf-8')
    except:
        print("Error : Cannot find file or read data")
    else:
        for key in hofPlayer:
            string = str(key)+':'+str(hofPlayer[key][0])+':'+str(hofPlayer[key][1])+':'+str(hofPlayer[key][2])+':'+str(hofPlayer[key][3])+ '\n'
            new.write(string)
        new.close()

def check():
    global count
    global table
    global nameX
    global nameO
    
    if (table[0] == table[1]) and (table[1] == table[2]):         
        if (table[0] == 'x'):
            onEndgame(nameX, nameO)
        if (table[0] == 'o'):
            onEndgame(nameO, nameX)
        count = 99
        
    elif (table[0] == table[3]) and (table[3] == table[6]):         
        if (table[0] == 'x'):
            onEndgame(nameX, nameO)
        if (table[0] == 'o'):
            onEndgame(nameO, nameX)
        count = 99
        
    elif (table[0] == table[4]) and (table[4] == table[8]):         
        if (table[0] == 'x'):
            onEndgame(nameX, nameO)
        if (table[0] == 'o'):
            onEndgame(nameO, nameX)
        count = 99
        
    elif (table[3] == table[4]) and (table[4] == table[5]):         
        if (table[3] == 'x'):
            onEndgame(nameX, nameO)
        if (table[3] == 'o'):
            onEndgame(nameO, nameX)
        count = 99
        
    elif (table[6] == table[7]) and (table[7] == table[8]):         
        if (table[6] == 'x'):
            onEndgame(nameX, nameO)
        if (table[6] == 'o'):
            onEndgame(nameO, nameX)
        count = 99
        
    elif (table[1] == table[4]) and (table[4] == table[7]):         
        if (table[1] == 'x'):
            onEndgame(nameX, nameO)
        if (table[1] == 'o'):
            onEndgame(nameO, nameX)
        count = 99
        
    elif (table[2] == table[5]) and (table[5] == table[8]):         
        if (table[2] == 'x'):
            onEndgame(nameX, nameO)
        if (table[2] == 'o'):
            onEndgame(nameO, nameX)
        count = 99
        
    elif (table[2] == table[4]) and (table[4] == table[6]):         
        if (table[2] == 'x'):
            onEndgame(nameX, nameO)
        if (table[2] == 'o'):
            onEndgame(nameO, nameX)
        count = 99   

def clientPlay(client):
    global table    
    global count
    global btns
    global btns2
    
    count += 1
    
    showinfo("GAME", ("Waiting for client(X) move"))
    
    tmp = bytes.decode(client.recv(20))
    (table[int(tmp) - 1]) = 'x'
    btns[int(tmp) - 1].set('X')
    btns2[int(tmp) - 1].configure(state=DISABLED)
    check()
    
def clientMultiXPlay(client2, client1):
    global table    
    global count
    global btns
    global btns2
    
    count += 1
    
    tmp = bytes.decode(client2.recv(20))
    client1.send(tmp.encode('ascii'))
    (table[int(tmp) - 1]) = 'x'
    btns[int(tmp) - 1].set('X')
    btns2[int(tmp) - 1].configure(state=DISABLED)
    check()
    
def clientMultiOPlay(client1, client2):
    global table    
    global count
    global btns
    global btns2
    
    count += 1
    
    tmp = bytes.decode(client1.recv(20))
    client2.send(tmp.encode('ascii'))
    (table[int(tmp) - 1]) = 'o'
    btns[int(tmp) - 1].set('O')
    btns2[int(tmp) - 1].configure(state=DISABLED)
    check()

def serverPlay(client):
    global table
    global count
    global btns
    global btns2
    
    count += 1
    
    button1.wait_variable(xoSet)

    table[int(xoSet.get()) - 1] = 'o'
    btns[int(xoSet.get()) - 1].set('O')
    btns2[int(xoSet.get()) - 1].configure(state=DISABLED)
    client.send(str(xoSet.get()).encode('ascii'))
    check()
    
def onEndgame(win, lose):
    global hofPlayer
    
    try:
        hofPlayer[str(win)][0] += 1
        hofPlayer[str(win)][1] += 1
    except:
        hofPlayer.update({str(win):[1, 1, 0, 0]})
    
    try:
        hofPlayer[str(lose)][0] += 1
        hofPlayer[str(lose)][2] += 1
    except:
        hofPlayer.update({str(lose):[1, 0, 1, 0]})
    
    writeHoF()
        
    showinfo("CONGRATULATION", ("The winner is " + str(win)))
    onReset()
    
def onDraw(name1, name2):
    try:
        hofPlayer[str(name1)][0] += 1
        hofPlayer[str(name1)][3] += 1
    except:
        hofPlayer.update({str(name1):[1, 0, 0, 1]})
    
    try:
        hofPlayer[str(name2)][0] += 1
        hofPlayer[str(name2)][3] += 1
    except:
        hofPlayer.update({str(name2):[1, 0, 0, 1]})
        
    writeHoF()
        
    showinfo("DRAW", ("!!DRAW!!"))
    onReset()
    
def onReset():
    showinfo("WARNNING", ("Game'll restart."))
    os.execl(sys.executable, os.path.abspath(__file__), *sys.argv)
        

def onConnect(hostname, port) :

    global name
    global count
    global btns
    global btns2
    global nameX
    global nameO
    
    run = False
    if (name.get() != '') and (port != ''):
        try:
            server.bind((hostname, int(port)))
            server.listen(5)
        except:
            pass
            showinfo("WARNNING", ("Port is busy or invalid"))
        else:
            run = True
            btnconnect.configure(state=DISABLED)
            txtPort.configure(state=DISABLED)
            txtName.configure(state=DISABLED)
            
    else:
        showinfo("WARNNING", ("Please input port and name."))
        
    server.settimeout(60)
    try: 
        while run:
            showinfo("WARNNING", ("Waiting for client"))
            client1, address1 = server.accept()
            client1.settimeout(60)
                
            for i in btns2:
                i.configure(state=ACTIVE)
                    
            mode = bytes.decode(client1.recv(20))
            client1Name = str(bytes.decode(client1.recv(20)))
                
            if int(mode) == 1 :
                msg = name.get()
                client1.send(msg.encode('ascii'))
                
                nameX = client1Name
                nameO = name.get()
                    
                count = 0
                    
                while count < 9:
                    clientPlay(client1)
                    if count >= 9:
                        break
                    serverPlay(client1)
                    if count >= 9:
                        break
                        
                if count != 99:
                    onDraw(nameX, nameO)
                client1.close()
                print(str(nameX) + " exit game\n")
                    
            if int(mode) == 2 :
                client1.send(('client1').encode('ascii'))
                client2, address2 = server.accept()
                client2.settimeout(60)
                
                mode = bytes.decode(client2.recv(20))
                client2Name = str(bytes.decode(client2.recv(20)))
                    
                if int(mode) == 1:
                    msg = name.get()
                    client2.send(msg.encode('ascii'))
                    
                    nameX = client2Name
                    nameO = name.get()
    
                    count = 0
                    
                    while count < 9:
                        clientPlay(client2)
                        if count >= 9:
                            break
                        serverPlay(client2)
                        if count >= 9:
                            break
                        
                    if count != 99:
                        onDraw(nameX, nameO)
                        
                    client2.close()
                    print(str(address2) + " exit game\n")
                    client1.close()
                    print(str(address1) + " exit game\n")
                    
                if int(mode) == 2:
                    client2.send(('client2').encode('ascii'))
                    
                    client1.send(client2Name.encode('ascii'))
                    client2.send(client1Name.encode('ascii'))
                    
                    nameX = client2Name
                    nameO = client1Name
                    count = 0
                    
                    while count < 9:
                        clientMultiXPlay(client2, client1)
                        if count >= 9:
                            break
                        clientMultiOPlay(client1, client2)
                        if count >= 9:
                            break
                        
                    if count != 99:
                        onDraw(nameX, nameO)
                        
                    client1.close()
                    print(str(address1) + " exit game\n")
                    client2.close()
                    print(str(address2) + " exit game\n")
                    
            else:
                pass
            break
        
    except socket.timeout:
        showinfo("WARNNING", ("Client not response, it's timeout."))
        onReset()
    
    except:
        showinfo("WARNNING", ("Something wrong."))
        onReset()
     
        
        
#------------------------------------Function CHANGE COLOR-------------------------------------------#
    
def changeColor(color):
    root.configure(background = color)
    Tops.configure(background = color)
    lblTitle = Label(Tops,font=('arial',50,'bold'),text="OX GAME SERVER",bd=20,fg='black'
                 ,bg=color,justify=CENTER).grid(row=0,column=0,sticky='nsew')
    MainFrame.configure(background = color)
    LeftFrame.configure(background = color)
    TopMainFrame.configure(background = color)
    txtFrame.configure(background = color)
    ButtomFrame.configure(background = color)
    choice1.configure(background = color)
    choice2.configure(background = color)
    choice3.configure(background = color)
    choice4.configure(background = color)
    lblColor = Label(ButtomFrame,font=('arial',10,'bold'),text="Select Background Color : ",bg=color
                     ,fg='black').grid(row=0,column=0,sticky='w')

#------------------------------------Window-------------------------------------------#

root = Tk()

root.title("OX Game Server")
root.geometry("830x670+0+0")
root.iconbitmap('OX_icon.ico')
root.resizable(False,False)

#------------------------------------Frame-------------------------------------------#

root.configure(background = '#EF476F')

Tops = Frame(root,bg = '#EF476F', pady = 2, width = 700, height = 100, relief = RIDGE)
Tops.grid(row=0,column=0)

TopFrame = Frame(root,bg = '#f5f5f5', pady = 2, width = 700, height = 70, relief = RIDGE)
TopFrame.grid(row=1,column=0)
TopFrame.config(highlightbackground='black', highlightthickness=2)

MainFrame = Frame(root, bg='#EF476F',bd=10,width=700,height=500,relief=RIDGE)
MainFrame.grid(row=2,column=0)
MainFrame.config(highlightbackground='black', highlightthickness=2)

LeftFrame = Frame(MainFrame, bd=10,width=550,height=500,pady=2,padx=10,bg='#EF476F',relief=RIDGE)
LeftFrame.pack(side=LEFT)

TopMainFrame = Frame(MainFrame, bd=5,width=300,height=100,pady=2,padx=2,bg='#EF476F', relief = RIDGE)
TopMainFrame.pack(side=TOP)

txtFrame = Frame(MainFrame,bd=5,width=300,height=100,pady=2,padx=2,bg='#EF476F', relief = RIDGE)
txtFrame.pack(side=BOTTOM)

ButtomFrame = Frame(root, bd=10,width=550,height=50,pady=2,padx=10,bg='#EF476F',relief=FLAT)
ButtomFrame.grid(row=4,column=0)

scroll_bar = Scrollbar(txtFrame) 
scroll_bar.pack(side = RIGHT,fill = Y)

#------------------------------------ADD CHANGE COLOR-------------------------------------------#

color = ['#EF476F', '#FFD166', '#06d6a0', '#118ab2']
v = StringVar(root, "1")

choice1 = Radiobutton(ButtomFrame,font=('arial',10,'bold'),bg='#EF476F', text = "Red", value = 1, variable = v, command =lambda: changeColor('#EF476F'))
choice1.grid(row = 0, column = 1)
choice2 = Radiobutton(ButtomFrame,font=('arial',10,'bold'),bg='#EF476F', text = "Yellow", value = 2, variable = v, command =lambda: changeColor('#FFD166'))
choice2.grid(row = 0, column = 2)
choice3 = Radiobutton(ButtomFrame,font=('arial',10,'bold'),bg='#EF476F', text = "Green", value = 3, variable = v, command =lambda: changeColor('#06d6a0'))
choice3.grid(row = 0, column = 3)
choice4 = Radiobutton(ButtomFrame,font=('arial',10,'bold'),bg='#EF476F', text = "Blue", value = 4, variable = v, command =lambda: changeColor('#118ab2'))
choice4.grid(row = 0, column = 4)


#============================varible===============================

hofPlayer = {}

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

hostname = socket.gethostname()
ip = socket.gethostbyname(hostname)
port = StringVar()

count = 0
table = ['1','2','3','4','5','6','7','8','9']
btn1 = StringVar()
btn2 = StringVar()
btn3 = StringVar()
btn4 = StringVar()
btn5 = StringVar()
btn6 = StringVar()
btn7 = StringVar()
btn8 = StringVar()
btn9 = StringVar()
btns = [btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8, btn9]

nameX = 'X'
nameO = 'O'

name = StringVar()

xoSet = StringVar()

#============================Label===================================================

lblTitle = Label(Tops,font=('arial',50,'bold'),text="OX GAME SERVER",bd=20,fg='black'
                 ,bg='#EF476F',justify=CENTER).grid(row=0,column=0)

lblHost = Label(TopFrame,font=('arial',16,'bold'),text="Hostname :",bd=10,fg='black'
                ,bg='#f5f5f5',justify=CENTER).grid(row=0,column=0)
lblHost_name = Label(TopFrame,font=('arial',16,'bold'),text=hostname,bd=10,bg='#f5f5f5'
                     ,fg='black').grid(row=0,column=1,sticky='w')

lblIP = Label(TopFrame,font=('arial',16,'bold'),text="IP :",bd=10,fg='black'
              ,bg='#f5f5f5',justify=CENTER).grid(row=0,column=2,sticky='e')
lblIP_name = Label(TopFrame,font=('arial',16,'bold'),text=ip,bd=10,bg='#f5f5f5'
                     ,fg='black').grid(row=0,column=3,sticky='w')

lblName =  Label(TopFrame,font=('arial',16,'bold'),text="Name :",bd=10,fg='black'
              ,bg='#f5f5f5',justify=CENTER).grid(row=1,column=0,sticky='e')
txtName = Entry(TopFrame,font=('arial',16,'bold'),bd=2,width=16,justify='center',textvariable=name,relief = SUNKEN)
txtName.grid(row=1,column=1,sticky='w')

lblPort =  Label(TopFrame,font=('arial',16,'bold'),text="Port :",bd=10,fg='black'
              ,bg='#f5f5f5',justify=CENTER).grid(row=1,column=2,sticky='e')
txtPort = Entry(TopFrame,font=('arial',16,'bold'),bd=2,width=10,justify='center',textvariable=port,relief = SUNKEN)
txtPort.grid(row=1,column=3,sticky='w')

boxEm = Label(TopFrame,text=" ",font=('Times 16 bold'),bg='#f5f5f5').grid(row=1,column=5)

lblColor = Label(ButtomFrame,font=('arial',10,'bold'),text="Select Background Color : ",bg='#EF476F'
                     ,fg='black').grid(row=0,column=0,sticky='w')

#==========================button===================================================

btnconnect = Button(TopFrame, text="Connect",font=('Times 16 bold'),width=8,padx=10,pady=0,bg='gainsboro',command=lambda:onConnect(hostname, txtPort.get()))
btnconnect.grid(row=1,column=4,sticky='ew')

button1 = Button(LeftFrame, textvariable=btn1,font=('Times 26 bold'),height=2,width=6,bg='gainsboro',command=lambda:xoSet.set('1'))
button1.grid(row=1,column=0,sticky='nsew')

button2 = Button(LeftFrame, textvariable=btn2,font=('Times 26 bold'),height=2,width=6,bg='gainsboro',command=lambda:xoSet.set('2'))
button2.grid(row=1,column=1,sticky='nsew')

button3 = Button(LeftFrame, textvariable=btn3,font=('Times 26 bold'),height=2,width=6,bg='gainsboro',command=lambda:xoSet.set('3'))
button3.grid(row=1,column=2,sticky='nsew')

button4 = Button(LeftFrame, textvariable=btn4,font=('Times 26 bold'),height=2,width=6,bg='gainsboro',command=lambda:xoSet.set('4'))
button4.grid(row=2,column=0,sticky='nsew')

button5 = Button(LeftFrame, textvariable=btn5,font=('Times 26 bold'),height=2,width=6,bg='gainsboro',command=lambda:xoSet.set('5'))
button5.grid(row=2,column=1,sticky='nsew')

button6 = Button(LeftFrame, textvariable=btn6,font=('Times 26 bold'),height=2,width=6,bg='gainsboro',command=lambda:xoSet.set('6'))
button6.grid(row=2,column=2,sticky='nsew')

button7 = Button(LeftFrame, textvariable=btn7,font=('Times 26 bold'),height=2,width=6,bg='gainsboro',command=lambda:xoSet.set('7'))
button7.grid(row=3,column=0,sticky='nsew')

button8 = Button(LeftFrame, textvariable=btn8,font=('Times 26 bold'),height=2,width=6,bg='gainsboro',command=lambda:xoSet.set('8'))
button8.grid(row=3,column=1,sticky='nsew')

button9 = Button(LeftFrame, textvariable=btn9,font=('Times 26 bold'),height=2,width=6,bg='gainsboro',command=lambda:xoSet.set('9'))
button9.grid(row=3,column=2,sticky='nsew')

btns2 = [button1, button2, button3, button4, button5, button6, button7, button8, button9]

for i in btns2:
    i.config(state=DISABLED)

btnhof = Label(TopMainFrame, text="Hall of fame",font=('Times 18 bold'),height=1,width=15,padx=25,pady=9,bg='#25383C',fg='#E5E4E2')
btnhof.grid(row=1,column=0)

txthof = Text(txtFrame,font=('TH Sarabun New',12,'bold'), bd=5,width=35,height=14,bg='#25383C',fg='#E5E4E2',yscrollcommand = scroll_bar.set,)
txthof.pack( side = LEFT, fill = BOTH )

hoftext=" No - Name : Game : Win : Lose : Draw\n"
txthof.insert(END, hoftext + '\n')

readHoF()

txthof.configure(state=DISABLED)

scroll_bar.config( command = txthof.yview ) 
root.mainloop()