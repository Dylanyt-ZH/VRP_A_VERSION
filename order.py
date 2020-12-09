from constants import *
class Order :
    def __init__(self,customer,orderCreateTime,requestTime,requestPositionX,requestPositionY,orderAmount,realReachTime=DEFAULTREACHTIME):
        self.Customer=customer #客户(订单编号)
        self.OrderCreateTime=orderCreateTime #下单时间
        self.RequestTime=int(requestTime) #订单要求送达时间
        self.RequestPosition=[requestPositionX,requestPositionY]  #订单要求送达的地点
        self.RequestPositionX=requestPositionX
        self.RequestPositionY=requestPositionY
        self.OrderAmount=orderAmount #订单订购量
        self.RealReachTime=int(realReachTime) #订单到达时间,初始化时为0
        self.Distance=self.CalDistance()
        self.LastestOutTime=self.LastestOutTime() #订单的最晚出发时间
        self.istaken=False #订单是否被配送员接受，False为未被接受
        
    
    # 当某一订单送达后，修改它的实际送达时间
    def OrderAchieved(self,time):
        self.RealReachTime=time

    # 计算订单的最晚发车时间
    def LastestOutTime(self):
        distance=int((self.RequestPositionX**2+self.RequestPositionY**2)**0.5)
        # print(distance)
        lastestouttime=int(self.RequestTime-(distance/SPEED))
        return lastestouttime
    
    #计算任务点到出发点距离
    def CalDistance(self):
        distance=int((self.RequestPositionX**2+self.RequestPositionY**2)**0.5)
        return distance

    # 格式化打印订单信息
    def Printinfo(self):
        print("The Customer is {}.\n\
The OrderCreateTime is {},\n\
Resquest Time is  {},\n\
ResquestPosition is {},\n\
Distance is {},\n\
Amount is {}\n\
The last out time is {}\n\
The Real reach Time is {}\n\
The order is taken :{} \
".format(self.Customer,self.OrderCreateTime,self.RequestTime,self.RequestPosition,self.Distance,self.OrderAmount,self.LastestOutTime,self.RealReachTime,self.istaken))


    