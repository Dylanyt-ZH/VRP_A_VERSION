# 路径规划滞后算法:
# 在骑手出发之前尽可能多获取订单信息，到最晚发车时间出发，
# 可能会造成订单浪费，需要第二位骑手重新进行听单-规划-派送
import random
import matplotlib.pyplot as pyplot
import numpy as np
from time import ctime
import time
from order import *
from rider import *

order_list = []
real_time = 0
full_order_amount = 0
lastoutTimeList = []
# 创建一个骑手对象
rider = Rider()


def drawplot(order_list):
    pyplot.xlim(-5000, 5000)
    pyplot.ylim(-5000, 5000)
    # 设置坐标系的原点在中心
    ax = pyplot.gca()
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.spines['bottom'].set_position(('data', 0))
    ax.spines['left'].set_position(('data', 0))
    for order in order_list:
        pyplot.scatter(order.RequestPositionX, order.RequestPositionY, c="b")
        pyplot.annotate(order.Customer, (order.RequestPositionX, order.RequestPositionY))
    pyplot.show()


# 展示所有订单的信息
def showOrdersInfo(order_list):
    for order in order_list:
        order.Printinfo()
        print("----------------------")

def createOrders(real_time):
    global full_order_amount
    global order_list
    customer = full_order_amount + 1
    orderCreateTime = real_time
    requestTime = orderCreateTime + 40
    # 随机生成距离商店5km之内的任务点
    requestPositionX = random.randint(-5000, 5000)
    requestPositionY = random.randint(-5000, 5000)
    orderAmount = random.randint(1, 5)
    order = Order(customer, orderCreateTime, requestTime, requestPositionX, requestPositionY, orderAmount)
    order_list.append(order)
    full_order_amount += 1
    global lastoutTimeList
    lastoutTimeList.append(order.LastestOutTime)
    global rider
    rider.Mission.append(order.Customer)

# 模拟时间流逝
def ListenTime():
    global real_time
    global lastoutTimeList
    if lastoutTimeList:
        lastoutTime = min(lastoutTimeList)
    else:
        lastoutTime = INFINTE
    while real_time < lastoutTime:
        # time.sleep(1)
        real_time = real_time + 1
        # print("real_time is {}".format(real_time))
        # 使用随机数随机生成订单
        random_flag = random.randint(1, 3)
        if real_time % random_flag == 0:
            # print("an order Created")
            createOrders(real_time)
        if lastoutTimeList:
            lastoutTime = min(lastoutTimeList)

# 计算各店之间的距离，生成距离矩阵
def CalDistance(order_list, full_order_amount):
    distanceMatrix = [[0 for i in range(full_order_amount + 1)] for i in range(full_order_amount + 1)]
    # 生成商店位置，便于位置计算
    shop = Order(0, 0, 0, 0, 0, 0)
    order_list.insert(0, shop)
    for i in range(full_order_amount + 1):
        for j in range(full_order_amount + 1):
            distance = int(((order_list[i].RequestPositionX - order_list[j].RequestPositionX) ** 2 + \
                            (order_list[i].RequestPositionY - order_list[j].RequestPositionY) ** 2) ** 0.5)
            distanceMatrix[i][j] = distance
    # 删除商店位置信息，防止后期计算出错
    order_list.pop(0)
    return distanceMatrix

# 输出距离矩阵
def showDistanceMatrix(distanceMartix):
    for line in distanceMartix:
        print(line)



# 计算出骑手当前路径下的最晚发车时间
def CalLastOutTime(rider, order_list, distanceMartix):
    global real_time
    PathLastOutTime = INFINTE
    for i in range(len(rider.PathCollection)):
        if i==0 or i==len(rider.PathCollection)-1:
            continue
        elif i==1:
            order_list[rider.PathCollection[i]-1].RealReachTime = order_list[rider.PathCollection[i]-1].RequestTime
            newPathOutTime=order_list[rider.PathCollection[i]-1].LastestOutTime
        else:
            # order_list[rider.PathCollection[i]-1].RequestTime :Tj
            # order_list[rider.PathCollection[i-1]-1].RealReachTime :ti
            # distanceMatrix[i][j]= dij
            Tj=order_list[rider.PathCollection[i]-1].RequestTime
            ti=order_list[rider.PathCollection[i-1]-1].RealReachTime
            dij=distanceMartix[rider.PathCollection[i-1]][rider.PathCollection[i]]
            t0=rider.riderLastoutTime
            newPathOutTime=int(Tj-((ti+(dij/SPEED))-t0))

        if newPathOutTime<=PathLastOutTime:
            PathLastOutTime=newPathOutTime
    print("Path Last out time is {}".format(PathLastOutTime))
    return PathLastOutTime   
    


# 计算出骑手的路径
def CalPath(order_list, rider, distanceMartix):
    flag = 0
    # 找到骑手需要第一个送的订单
    for order in order_list:
        if order.LastestOutTime == rider.riderLastoutTime and order.istaken == False:
            rider.PathCollection.insert(1,order.Customer)
            order.istaken = True  # 该订单已被骑手接受，改变订单状态
            flag = order.Customer
            rider.Mission.pop(flag-1)
            break
    rider.showinfo()
    PathLastOutTime=CalLastOutTime(rider, order_list, distanceMartix)
    showDistanceMatrix(distanceMartix)
    # 找到第一个订单后，寻找与最新加入的点距离最小的点(除去原点和自己本身)
    minpoint=INFINTE
    line=flag
    for index in range (len(distanceMartix[line])):
        # 寻找其他点的过程中如果找到自己，则跳过
        if index==line:
            continue
        else:
            if distanceMartix[line][index]<minpoint:
                minpoint=distanceMartix[line][index]
                flag=index
    print("The minpiont is {} and flag is {}".format(minpoint,flag))
    # 找到了新的距离最小点，计划加入骑手的路线 ins_pos:插入的位置
    ins_pos=-1
    deltadistancelist=[] 
    for i in range (len(rider.PathCollection)-1):
        deltadistancelist.append(
            distanceMartix[rider.PathCollection[i]][flag]+distanceMartix[flag][rider.PathCollection[i+1]]-distanceMartix[rider.PathCollection[i]][rider.PathCollection[i+1]])
    mindistance=INFINTE
    for i in range(len(deltadistancelist)):
        if deltadistancelist[i]<=mindistance:
            mindistance=deltadistancelist[i]
            ins_pos=i+1

    print("insert position is {}".format(ins_pos))
    rider.PathCollection.insert(ins_pos,flag)
    PathLastOutTime=CalLastOutTime(rider, order_list, distanceMartix)
    rider.showinfo()
        



def main():
    # 模拟听单阶段
    ListenTime()
    # showOrdersInfo(order_list)
    # 计算各个点之间的距离,生成距离矩阵
    print("full_order_amount=== {}".format(full_order_amount))
    
    distanceMartix = CalDistance(order_list, full_order_amount)
    print("Last out time list is {}".format(lastoutTimeList))
    rider.riderLastoutTime = min(lastoutTimeList)
    rider.showinfo()
    CalPath(order_list, rider, distanceMartix)
    # drawplot(order_list)
    print("The real time is {}".format(real_time))


main()
