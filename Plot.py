# coding: utf-8
from tkinter import *
import pandas as pd


def getTspData(path,route):
    city_location = pd.read_csv(path)
    x_coor = city_location['x-coordinate']
    y_coor = city_location['y-coordinate']

    Pot_set = []
    Pot_seq = []
    #Pot_set
    for i in range(len(x_coor)):
        x = x_coor[i]
        y = y_coor[i]
        Pot_set.append((50+6.5*x, 475-4.5*y))
    #Pot_seq
    print(type(route))
    for num in route:
        x = x_coor[num]
        y = y_coor[num]
        Pot_seq.append((50+6.5*x, 475-4.5*y))

    return Pot_set,Pot_seq

def getVrpData(path,route_set):
    pot_locatin = pd.read_csv(path)
    x_coor = pot_locatin['x-coordinate']
    y_coor = pot_locatin['y-coordinate']

    Pot_set = []
    Pot_seq = []
    #Pot_set
    for i in range(len(x_coor)):
        x = x_coor[i]
        y = y_coor[i]
        Pot_set.append((50+6.5*x, 475-4.5*y))
    #Pot_set
    for route in route_set:
        seq = []
        for num in route:
            x = x_coor[num]
            y = y_coor[num]
            seq.append((50+6.5*x, 475-4.5*y))
        Pot_seq.append(seq)      

    return Pot_set,Pot_seq


def TspPlot(path,route,canvas):
    #path = 'city_location.csv'
    #route = [8, 24, 4, 5, 25, 2, 26, 0, 1, 28, 18, 16, 6, 10, 15, 19, 27, 17, 23, 21, 20, 29, 13, 12, 3, 7, 11, 9, 22, 14, 8]
    '''
    root = Tk()
    root.title('line chart')
    canvas = Canvas(root, width=750, height=500, bg='white')
    canvas.pack()
    '''
    
    #绘制坐标轴线
    canvas.create_line(50, 475, 720, 475, width=2,arrow=LAST)  #x轴
    canvas.create_line(50, 475, 50, 5, width=2,arrow=LAST) #y轴

    #绘制x刻度
    for i in range(21):
        x = 50 + i*32.5
        canvas.create_line(x, 475, x, 480, width=2)
        canvas.create_text(x, 481 ,text='%d'%(i*5),anchor=N)

    #绘制y刻度
    for i in range(21):
        y = 475 - (i*22.5)
        canvas.create_line(50,y,54,y,width=2)
        canvas.create_text(48,y,text='%d'%(5*i),anchor=E)

    #绘制折线
    pot_set,pot_seq = getTspData(path,route)
    canvas.create_line(pot_seq, fill='black')

    #绘制散点
    for x,y in pot_set:
        canvas.create_oval(x-4, y-4, x+4, y+4, width=1, outline='black', fill='blue')

    #绘制城市标号
    for i in range(len(pot_set)):
        (x,y) = pot_set[i]
        canvas.create_text(x-5, y-5, text='%d'%(i),anchor=E,font='SimHei 10 bold')

    #root.mainloop()

def VrpPlot(path,route,canvas):
    #path = 'data.csv'
    #route = [[0, 29, 0], [0, 14, 5, 26, 19, 7, 6, 9, 0], [0, 21, 3, 22, 11, 23, 16, 0], [0, 13, 4, 25, 20, 12, 0], [0, 2, 17, 8, 30, 18, 24, 0], [0, 1, 28, 10, 27, 15, 0]]
    '''
    root = Tk()
    root.title('line chart')
    canvas = Canvas(root, width=750, height=500, bg='white')
    canvas.pack()
    '''
    
    #绘制坐标轴线
    canvas.create_line(50, 475, 700, 475, width=2)  #x轴
    canvas.create_line(50, 475, 50, 25, width=2) #y轴

    #绘制x刻度
    for i in range(21):
        x = 50 + i*32.5
        canvas.create_line(x, 475, x, 480, width=2)
        canvas.create_text(x, 481 ,text='%d'%(i*5),anchor=N)

    #绘制y刻度
    for i in range(21):
        y = 475 - (i*22.5)
        canvas.create_line(50,y,54,y,width=2)
        canvas.create_text(48,y,text='%d'%(5*i),anchor=E)


    #绘制折线
    pot_set,pot_seq = getVrpData(path,route)

    for seq in pot_seq:
        canvas.create_line(seq, fill='black')

    #绘制散点
    for  i in range(len(pot_set)):
        if i != 0:
            (x,y) = pot_set[i]
            canvas.create_oval(x-4, y-4, x+4, y+4, width=1, outline='black', fill='blue')
        else:
            (x,y) = pot_set[i]
            canvas.create_oval(x-5, y-5, x+5, y+5, width=1, outline='yellow', fill='red')


    #绘制城市标号
    for i in range(len(pot_set)):
        (x,y) = pot_set[i]
        canvas.create_text(x-5, y-5, text='%d'%(i),anchor=E,font='SimHei 10 bold')
    #root.mainloop()