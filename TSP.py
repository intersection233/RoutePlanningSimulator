#Assignment Problem + Patching Heuristic求解TSP问题

import pandas as pd
from scipy.optimize import linear_sum_assignment
import math

def getDistanceMa(location):
    x_coor = location['x-coordinate']
    y_coor = location['y-coordinate']
    distance = [[]for i in range(len(x_coor))]
    for i in range(len(x_coor)):
        for j in range(len(y_coor)):
            if i == j:
                distance[i].append(float("inf"))
            else:
                distance[i].append(math.sqrt(pow(x_coor[i]-x_coor[j],2)+pow(y_coor[i]-y_coor[j],2)))
    return distance

def getRouteSet(row_ind,col_ind):
    route_set = []
    for i in range(len(row_ind)):
        route_tmp = []
        route_tmp.append(row_ind[i])
        route_tmp.append(col_ind[i])
        route_set.append(route_tmp)
    #print(route_set)
    for i in range(len(route_set)):
        for j in range(i+1,len(route_set)):
            if route_set[i][-1] == route_set[j][0]:
                #print(route_set[i])
                #print(route_set[j])
                route_set[j].remove(route_set[j][0])
                route_new = route_set[i] + route_set[j]
                route_set[j] = route_new
                break
    route_set_final = []
    for i in range(len(route_set)):
        if route_set[i][0] == route_set[i][-1]:
            route_set_final.append(route_set[i])
    return route_set_final

def subSort(array,low,high):
    tmp = array[low]
    while low < high:
        while low < high and array[high][0] >= tmp[0]:
            high -= 1
        array[low] = array[high]
        while low < high and array[low][0] <= tmp[0]:
            low += 1
        array[high] = array[low]
    array[low] = tmp
    return low

#按照array[0]从小到大排列
def quickSort(array,low,high):
    #array为二维列表
    if low < high:
        location = subSort(array,low,high)
        quickSort(array, low, location -1)
        quickSort(array, location+1, high)

def calDistance(route,distance):
    distance_sum = 0
    for i in range(len(route)-1):
        distance_tmp = distance[int(route[i])][int(route[i+1])]
        distance_sum += distance_tmp
    return distance_sum
    
def Combine(route1, route2,distance):
    len1 = len(route1)
    len2 = len(route2)
    distance_list = []
    if len1 > len2 or len1 == len2:
        #route2顺序链接
        for i in range(len1-1):
            distance_tmp = []
            route1_seq1 = route1[0:i+1]
            #print("route1_seq1 :",route1_seq1)
            route1_seq2 = route1[i+1:len1]
            #print("route1_seq2: ", route1_seq2)
            route2_tmp = route2[1:len(route2)+1]
            #print("route2_tmp: ",route2_tmp)
            route_new = route1_seq1 + route2_tmp + route1_seq2
            #print(route_new)
            distance_tmp.append(calDistance(route_new,distance))
            distance_tmp.append(route_new)
            #print(distance_tmp)
            distance_list.append(distance_tmp)  
        #route2逆序链接
        for i in range(len1-1):
            distance_tmp = []
            route1_seq1 = route1[0:i+1]
            #print("route1_seq1 :",route1_seq1)
            route1_seq2 = route1[i+1:len1]
            #print("route1_seq2: ", route1_seq2)
            route2_tmp = route2[0:len(route2)-1]
            #print("route2_tmp: ",route2_tmp)
            route_new = route1_seq1 + route2_tmp + route1_seq2
            #print(route_new)
            distance_tmp.append(calDistance(route_new,distance))
            distance_tmp.append(route_new)
            #print(distance_tmp)
            distance_list.append(distance_tmp)  
        #print('distance_list:',distance_list)
        quickSort(distance_list,0,len(distance_list)-1)
        route = distance_list[-1][1]  
    else:
        route = Combine(route2,route1,distance)
    return [len(route),route]
            

#patching heuristic
def Patching(route_set,distance):
    route_sort = [[]for i in range(len(route_set))]
    for i in range(len(route_set)):
        route_tmp = []
        route_tmp.append(len(route_set[i]))
        route_tmp.append(route_set[i])
        route_sort[i] = route_tmp
    quickSort(route_sort,0,len(route_sort)-1)
    #print(route_sort)
    #print(route_sort)
    while len(route_sort) > 1:
        #print("******************")
        route1 = route_sort[-1][1]
        route2 = route_sort[-2][1]
        route_sort.remove(route_sort[-1])
        route_sort.remove(route_sort[-1])
        #print("route1: ", route1)
        #print("route2: ", route2)
        new_route = Combine(route1, route2,distance) #根据增加的距离数最短来合并路
        route_sort.append(new_route)
    return route_sort[0][1]

def addArrow(route):
    path = []
    for i in range(len(route)):
        if i != len(route)-1:
            pot = route[i]
            path.append(str(pot))
            path.append('->')
        else:
            pot = route[i]
            path.append(str(pot))
    return path



def run(path):
    city_location = pd.read_csv(path)
    distance = getDistanceMa(city_location)
    row_ind,col_ind=linear_sum_assignment(distance)
    route_set = getRouteSet(row_ind,col_ind)
    final_route = Patching(route_set,distance)
    final_path = addArrow(final_route)
    #print(final_route)
    return final_path,final_route
