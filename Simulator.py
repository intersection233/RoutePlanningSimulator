from tkinter import *
from tkinter import filedialog,ttk
import TSP
import VRP
import Plot

#选择问题类型
def getRoutePlan(ProblemType,carCap,TspUpload,TspPlot,TspSolve,VrpUpload,VrpPlot,VrpSolve,Route,Path,tip,Route_list,canvas):
    num = ProblemType.get()
    if num == 1:
        canvas.delete(ALL)
        Route_list[:] = []
        Route.set('')
        Path.set('')
        carCap.config(state = 'readonly')
        TspUpload["state"] = NORMAL
        TspPlot["state"] = NORMAL
        TspSolve["state"] = NORMAL
        VrpUpload["state"] = DISABLED
        VrpPlot["state"] = DISABLED
        VrpSolve["state"] = DISABLED
        tip.set('Plaese upload file')
    else:
        canvas.delete(ALL)
        Route_list[:] = []
        Route.set('')
        Path.set('')
        carCap.config(state = 'normal')
        TspUpload["state"] = DISABLED
        TspPlot["state"] = DISABLED
        TspSolve["state"] = DISABLED
        VrpUpload["state"] = NORMAL
        VrpPlot["state"] = NORMAL
        VrpSolve["state"] = NORMAL
        tip.set('Plaese input capacity and upload file')


#获取文件名
def getfile(fpath,tip):
    file_path=filedialog.askopenfilename()
    fpath.set(file_path)
    if file_path != '':
        tip.set('Successfully uploaded, please click "Slove" to slove')
    else:
        tip.set('Please upload again')


def tspSolve(fpath,Route,Path,tip,Route_list):
    root = fpath.get()
    route = []
    path = []
    path,route = TSP.run(root)
    #print('route: ',route)
    #print('path: ',path)
    Route_list[:] = route
    Route.set(route)
    Path.set(path)
    tip.set('Solved! Please click "Plot" to plot')


def vrpSolve(fpath,Route,Path,carCap,tip,Route_list):
    root = fpath.get()
    car_cap = carCap.get()
    if car_cap == '':
        tip.set('Please input capacity')
    else:
        route = []
        path = []
        path,route = VRP.run(root,int(car_cap))
        #print('route: ',route)
        #print('path: ',path)
        Route_list[:] = route
        Route.set(route)
        Path.set(path)
        tip.set('Solved!')

def tspPlot(root,Route_list,tip,canvas):
    Root = root.get()
    Plot.TspPlot(Root,Route_list,canvas)
    tip.set('Plotted!')

def vrpPlot(root,Route_list,tip,canvas):
    Root = root.get()
    Plot.VrpPlot(Root,Route_list,canvas)
    tip.set('Plotted')



def layout(root):
    fpath = StringVar()
    ProblemType = IntVar()  #选择问题类型，1表示TSP问题，2表示VRP问题
    Route = StringVar()
    Route_list = []         #list
    Path = StringVar()
    tip = StringVar()

    Label(root, text = 'Path Planning Problem Simulator',font='SimHei 20 bold').place(x=220,y=10)

    #坐标系画布
    GraphFrame = Frame(root,relief=GROOVE,borderwidth=2)#脊状边缘的
    GraphFrame.place(x=5,y=60,width=750,height=500)
    #Label(GraphFrame, text='坐标图').pack()
    canvas = Canvas(GraphFrame,width=750,height=500,bg='white')
    canvas.pack()

    #TSP
    TSPFrame = Frame(root,relief=GROOVE,borderwidth=2)#脊状边缘的
    TSPFrame.place(x=765,y=60,width=230,height=100)
    Label(TSPFrame, text='TSP').grid(row=0,column=1)
    rd1 = Radiobutton(TSPFrame,text="TSP Problem",variable=ProblemType,value=1,command= lambda:getRoutePlan(ProblemType,carCap,TspUpload,TspPlot,TspSolve,VrpUpload,VrpPlot,VrpSolve,Route,Path,tip,Route_list,canvas))
    rd1.grid(row=2,column=0)
    TspUpload = Button(TSPFrame,text='Upload File',state=DISABLED,command= lambda: getfile(fpath,tip))
    TspUpload.grid(row=3,column=0)
    TspSolve = Button(TSPFrame,text='Slove',state=DISABLED,command= lambda: tspSolve(fpath,Route,Path,tip,Route_list))
    TspSolve.grid(row=3,column=1)
    TspPlot = Button(TSPFrame,text='Plot',state=DISABLED,command= lambda: tspPlot(fpath,Route_list,tip,canvas))
    TspPlot.grid(row=3,column=2)

    #VRP
    VRPFrame = Frame(root,relief=GROOVE,borderwidth=2)#脊状边缘的
    VRPFrame.place(x=765,y=160,width=230,height=120)  #
    Label(VRPFrame, text='VRP').grid(row=0,column=1)
    rd1 = Radiobutton(VRPFrame,text="VRP Problem",variable=ProblemType,value=2,command= lambda:getRoutePlan(ProblemType,carCap,TspUpload,TspPlot,TspSolve,VrpUpload,VrpPlot,VrpSolve,Route,Path,tip,Route_list,canvas))
    rd1.grid(row=2,column=0)
    Label(VRPFrame, text = 'Car Capacity:').grid(row=3,column=0)
    carCap = Entry(VRPFrame,width=10,state='readonly')
    carCap.grid(row=3,column=1)
    VrpUpload = Button(VRPFrame,text='Upload File',state=DISABLED,command= lambda: getfile(fpath,tip))
    VrpUpload.grid(row=4,column=0)
    VrpSolve = Button(VRPFrame,text='Slove',state=DISABLED,command= lambda: vrpSolve(fpath,Route,Path,carCap,tip,Route_list))
    VrpSolve.grid(row=4,column=1)
    VrpPlot = Button(VRPFrame,text='Plot',state=DISABLED,command= lambda: vrpPlot(fpath,Route_list,tip,canvas))
    VrpPlot.grid(row=4,column=2)

    TipFrame = Frame(root,relief=GROOVE,borderwidth=2)
    TipFrame.place(x=765,y=280,width=230,height=40)
    Label(TipFrame,text='Tips:').grid(row=0,column=0)
    VrpTip = Message(TipFrame, textvariable = tip, width=180)
    VrpTip.grid(row=0,column=1)

    ResulltFrame = Frame(root,relief=GROOVE,borderwidth=2)
    ResulltFrame.place(x=765,y=320,width=230,height=240)
    Label(ResulltFrame, text='Route Plan').grid(row=0,column=0)
    Message(ResulltFrame, textvariable = Path, width=200).grid(row=1,column=0)



def main():
    root = Tk()
    root.title('TSP&VRP Problem Simulator')
    root.geometry('1000x600')
    layout(root)
    root.mainloop()


if __name__=='__main__':
    main()