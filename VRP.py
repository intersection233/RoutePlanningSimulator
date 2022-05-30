import pandas as pd
import numpy as np

#定义快速排序函数,list为输入函数的列表,i为list中需要排序片段的开始下标，j为list中需要排序片段的结尾下标
def Quick_Sort(List,i,j):
    if i>=j:
        return List
    pivot_num = List[i][2]
    pivot = List[i]
    low = i
    high = j
    while i < j:
        while i < j and List[j][2] <= pivot_num:
            j -= 1
        List[i] = List[j]
        while i < j and List[i][2] >= pivot_num:
            i += 1
        List[j] = List[i]
    List[j] = pivot
    Quick_Sort(List,low,i-1)
    Quick_Sort(List,i+1,high)
    return List

#根据点查找路径
def Search_Route(route_list,point):
    RouteList = route_list
    for list in RouteList:
        if point in list:
            return list

#判断两点是否在同一条路径上,若在，返回True
def InOneRoute(route_list,i,j):
    routei = Search_Route(route_list,i)
    routej = Search_Route(route_list,j)
    if routei == routej:
        return True
    else:
        return False

#demand中第一个数为第一个客户点，下标为0
def GetDemand(demand,routei,routej):
    sum = 0
    for i in range(1,len(routei)-1):
        sum += demand[routei[i]-1]
    for j in range(1,len(routej)-1):
        sum += demand[routej[j]-1]
    return sum   

#获取route的距离
def GetDistance(distance,route):
    distance_num = 0
    for i in range(len(route)-1):
        now = route[i]
        next = route[i+1]
        distance_num += distance[now][next]
    return distance_num

#计算总费用
def Cal_TotalCost(travel_distance,car_num):
    fixed_cost = 500
    distance_sum = 0
    for distance in travel_distance:
        distance_sum += distance
    total_cost = fixed_cost*car_num + distance_sum
    return total_cost

#获取route上的需求
def GetCap(demand,route):
    sum = 0
    for i in range(1,len(route)-1):
        sum += demand[route[i]-1]
    return sum

#打印结果
def PrintResult(Route_Set,travel_distance,cost):
    for i in range(len(Route_Set)):
        print('Vehicle'+str(i+1)+': depot',end = "-")
        for j in range(1,len(Route_Set[i])-1):
            print('customer '+str(Route_Set[i][j]),end = "-")
        print('depot.')
    print('The travel distance of each vehicle is ',end = "")
    for distance in travel_distance:
        print(str("%.2f" % int(distance)), end = "; ")
    print("")
    print('The total cost of this solution is: '+str("%.2f" % int(cost)))

#路线间交换,对于任意的k、l两条路线，k中的一个点与l中的一个点进行交换
def PotExchange(Route_Set,distance,demand,car_cap):
    Route_Set = np.array(Route_Set)
    #获取Route_Set中任意两条路线,route1,route2
    for i in range(len(Route_Set)):
        for j in range(len(Route_Set)):
            if i != j:
                for x in range(1,len(Route_Set[i])-1):
                    for y in range(1,len(Route_Set[j])-1):
                        #route保存上一轮存下来的值，条件不符合时不进行变换
                        route1 = Route_Set[i].copy()
                        route2 = Route_Set[j].copy()
                        #route1_copy,route2_copy可以尝试性改变
                        route1_copy = route1.copy()
                        route2_copy = route2.copy()
                        #交换
                        tmp = route1_copy[x]
                        route1_copy[x] = route2_copy[y]
                        route2_copy[y] = tmp
                        demand1 = GetCap(demand,route1_copy)
                        demand2 = GetCap(demand,route2_copy)
                        #判断交换后两辆车是否都不超载
                        if (demand1 < car_cap) and (demand2 < car_cap):
                            #判断交换后distance是否会变短
                            distance1_ori = GetDistance(distance,route1)
                            distance2_ori = GetDistance(distance,route2)
                            distance1 = GetDistance(distance,route1_copy)
                            distance2 = GetDistance(distance,route2_copy)
                            sub_distance = distance1 + distance2 - distance1_ori - distance2_ori
                            if sub_distance < 0:
                                #交换两点
                                print(Route_Set)
                                tmp = route1[x]
                                route1[x] = route2[y]
                                route2[y] = tmp
                                #更新Route_Set
                                Route_Set[i] = route1
                                Route_Set[j] = route2
    return Route_Set

#对于任意的k路线，把k中的一个点放到另外任意一个路线l中任意一个位置
def PotInsert(Route_Set,distance,demand,car_cap):
    Route_Set = np.array(Route_Set)
    #获取Route_Set中任意两条路线,route1,route2
    for i in range(len(Route_Set)):
        for j in range(len(Route_Set)):
            if i != j:
                for x in range(1,len(Route_Set[i])-1):
                    for y in range(1,len(Route_Set[j])):
                        #route保存上一轮存下来的值，条件不符合时不进行变换
                        route1 = Route_Set[i].copy()
                        route2 = Route_Set[j].copy()
                        #route1_copy,route2_copy可以尝试性改变
                        route1_copy = route1.copy()
                        route2_copy = route2.copy()
                        #插入操作
                        route2_copy = np.insert(route2_copy,y,route1_copy[x])
                        route1_copy.remove(route1_copy[x])
                        #print(route2_copy)
                        demand1 = GetCap(demand,route1_copy)
                        demand2 = GetCap(demand,route2_copy)
                        #判断交换后两辆车是否都不超载
                        if (demand1 < car_cap) and (demand2 < car_cap):
                            #判断交换后distance是否会变短
                            distance1_ori = GetDistance(distance,route1)
                            distance2_ori = GetDistance(distance,route2)
                            distance1 = GetDistance(distance,route1_copy)
                            distance2 = GetDistance(distance,route2_copy)
                            sub_distance = distance1 + distance2 - distance1_ori - distance2_ori
                            if sub_distance < 0:
                                #插入操作
                                route1.remove(route1[x])
                                route2 = np.insert(route2,j,route1[x])
                                #更新Route_Set
                                Route_Set[i] = route1
                                Route_Set[j] = route2
    return Route_Set

#np.array转换为List
def getPathSet(route_set):
    path_set = []
    for i in range(len(route_set)):
        path_set.append(route_set[i])
    return path_set

#获取路线
def addArrow(route_set):
    path_set = []
    for i in range(len(route_set)):
        path = []
        for j in range(len(route_set[i])):
            if j != len(route_set[i])-1:
                pot = route_set[i][j]
                path.append(str(pot))
                path.append('->')
            else:
                pot = route_set[i][j]
                path.append(str(pot))
        path_set.append(path)
    return path_set



def run(path,Capacity):
    data = pd.read_csv(path)

    customer = data['customer']
    demand = data['demand']
    Xcoor = data['x-coordinate']
    Ycoor = data['y-coordinate']

    customer_num = customer.shape[0]-1

    Data = []

    for i in range(customer_num+1):
        Data.append([customer[i],demand[i],Xcoor[i],Ycoor[i]])

    #获取仓库与30个客户点之间的距离矩阵,用distance来存储，distance[i][j] = distance[j][i],代表客户i到客户j的距离
    distance = np.zeros((customer_num +1, customer_num +1))

    for i in range (customer_num+1):
        for j in range(customer_num+1 ):
            distance[i][j] = np.sqrt(pow((Data[i][2] - Data[j][2]),2)+pow((Data[i][3]-Data[j][3]),2))

    Route_Set = []

    for i in range(customer_num):
        Route_Set.append([0,i+1,0])

    first_pot = [] #用来存储与仓库相邻的第一个点
    last_pot = [] #用来存储与仓库相邻的最后一个点

    #当使用saving算法时，当点ij一个点为一条路径的起点，一个点为一条路径的终点时，才可以对两条路径进行合并
    for i in range(len(Route_Set)):
        first_pot.append(Route_Set[i][1])
        last_pot.append(Route_Set[i][1])

    #计算Saving，并记录在Saving[]中,注意Saving[i]表示客户i+1，Saving[j]表示表中客户j+1,注意客户i不能与自身交换
    Saving = np.zeros((customer_num,customer_num))

    for i in range(customer_num):
        for j in range(customer_num):
            if i == j:
                Saving[i][j] = 0
            else:
                Saving[i][j] = distance[0][i+1] + distance[0][j+1] - distance[i+1][j+1]

    #saving[]用来存放[i,j,Saving[i-1][j-1]]共有C(30)(2)个点,saving[i][j][k]表示客户i与客户j合并时可以节省k的距离
    saving = []
    for i in range(customer_num):
        for j in range(i+1,customer_num):
            saving.append([i+1,j+1,Saving[i][j]])

    #对saving进行排序
    saving_sort = Quick_Sort(saving,0,len(saving)-1)

    #划分车辆
    car_cap = Capacity
    capacity = 0 #记录当前车辆容量
    car_num =0 #记录使用的车辆数
    cost = 0 #记录总成本
    travel_distance = [] #记录每一条路径对应的行驶距离


    while saving_sort != []:#当saving非空
        Largest_Saving = saving_sort[0]
        saving_sort.pop(0)#弹出saving值最大的列表[i,j,saving[i][j]]
        i = Largest_Saving[0]
        j = Largest_Saving[1]
        #判断ij是否在同一条路径上
        if InOneRoute(Route_Set,i,j) != True: 
            #计算合并两条路后车辆的总载重
            routei = Search_Route(Route_Set,i)
            routej = Search_Route(Route_Set,j)
            capacity = GetDemand(demand,routei,routej)        
            #判断是否超出车辆容量
            if capacity < car_cap:
                if (i in first_pot) and (j in last_pot):#i为一条路线中第一个服务客户点，j为另一条路线中最后一个服务客户点
                    #合并两条路径
                    #print(i,j)
                    route1 = Search_Route(Route_Set,i)
                    #print(route1)
                    Route_Set.remove(route1)#从路径集合中去除此条路径
                    route1.pop(0)#除去路径中第一个点，即仓库
                    route2 = Search_Route(Route_Set,j)
                    #print(route2)
                    Route_Set.remove(route2)
                    route2.pop(-1)#除去路径中最后一个点，即仓库
                    new_route = route2 + route1
                    Route_Set.append(new_route)
                    first_pot.remove(i)
                    last_pot.remove(j)
                elif(i in last_pot) and (j in first_pot):#i为一条路径中最后一个服务客户点，j为另一条路线中第一个客户服务点
                    #合并两条路径
                    #print('two',i,j)
                    route1 = Search_Route(Route_Set,i)
                    #print(route1)
                    Route_Set.remove(route1)#从路径集合中去除此条路径
                    route1.pop(-1)#除去路径中最后一个点，即仓库
                    route2 = Search_Route(Route_Set,j)
                    #print(route2)
                    Route_Set.remove(route2)
                    route2.pop(0)#除去路径中第一个点，即仓库
                    new_route = route1 + route2
                    Route_Set.append(new_route)
                    first_pot.remove(j)
                    last_pot.remove(i)    
            else:
                #启用新的一辆车
                capacity = 0

    #将每条route的distance记录在travel_distance中
    for route in Route_Set:
        tmp_distance = GetDistance(distance,route)
        travel_distance.append(tmp_distance)

    #计算所用车辆数
    car_num = len(Route_Set) 
    cost = Cal_TotalCost(travel_distance,car_num)

    #优化1
    #路线间交换,对于任意的k、l两条路线，k中的一个点与l中的一个点进行交换
    Route_Set_after = PotExchange(Route_Set,distance,demand,car_cap)

    #travel_distance_after记录优化后的旅行距离，cost_after记录优化后的成本，Route_Set改变
    travel_distance_after = []
    for route in Route_Set_after:
        tmp_distance = GetDistance(distance,route)
        travel_distance_after.append(tmp_distance) 

    #优化2
    #对于任意的k路线，把k中的一个点放到另外任意一个路线l中任意一个位置
    Route_Set_after_insert = PotInsert(Route_Set_after,distance,demand,car_cap)
    #travel_distance_after_insert记录优化后的旅行距离，cost_after_insert记录优化后的成本，Route_Set改变
    travel_distance_after_insert = []
    for route in Route_Set_after_insert:
        tmp_distance = GetDistance(distance,route)
        travel_distance_after_insert.append(tmp_distance) 
    cost_after_insert = Cal_TotalCost(travel_distance_after_insert,car_num)

    #打印优化后结果
    #PrintResult(Route_Set_after_insert,travel_distance_after_insert,cost_after_insert)

    #print(Route_Set_after_insert)

    #不带箭头的路线集合
    Path_set = getPathSet(Route_Set_after_insert)
    print('Path_set:',Path_set)
    #带箭头的路线集合
    Path_Set = addArrow(Path_set)
    print('Path_Set:',Path_Set)

    return Path_Set,Path_set

