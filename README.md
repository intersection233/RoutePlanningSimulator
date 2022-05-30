# RoutePlanningSimulator

Simulator.py为主要代码，运行可以输出一个模拟器
TSP.py中包含求解TSP问题的算法（使用Assignment Probelm + Patching Heuristc算法求解）
VRP.py中包含求解VRP问题的求解算法（使用节约算法进行求解）
Plot.py中包含使用tkinter包绘制图形的代码

TspData为求解TSP问题的数据，数据格式：'x-coordinate','y-coordinate'，两列数据，包含需要遍历所有城市的坐标
VrpData为求解VRP问题的数据，数据格式：'customer','demand','x-coordinate','y-coordinate'，四列数据，包含仓库和客户点的坐标和需求，其中第一行为仓库数据，需求为0

Simulator.py is the main code, running can output a simulator
TSP.py contains algorithms for solving TSP problems (solved using the Assignment Probelm + Patching Heuristc algorithm)
VRP.py contains a solution algorithm for solving VRP problems (solving using a savings algorithm)
Plot.py contains code that uses the tkinter package to draw graphics

TspData is the data for solving TSP problems, the data format: 'x-coordinate', 'y-coordinate', two columns of data, including coordinates that need to be traversed through all cities
VrpData to solve the VRP problem data, data format: 'customer', 'demand', 'x-coordinate', 'y-coordinate', four columns of data, including the coordinates and requirements of the warehouse and customer points, of which the first line warehouse data, the requirements are 0
