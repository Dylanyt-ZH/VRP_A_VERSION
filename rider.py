from constants import *
class Rider:
    def __init__(self):
        self.Mission=[] #骑手的任务地点集
        self.PathCollection=[0,0] #骑手的路径集合
        self.riderLastoutTime=INFINTE #设置单个骑手的最晚出发时间，初始化时为正无穷
        
    def showinfo(self):
        print("****************")
        print("The rider's mission are {}".format(self.Mission))
        print("The rider's Path are {}".format(self.PathCollection))
        print("The rider's Last out time are {}".format(self.riderLastoutTime))
        print("****************")

