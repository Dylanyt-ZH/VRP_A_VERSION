from time import ctime
import threading
import time

def coding(language):
      for i in range(20):
        time.sleep(3)
        print('I\'m coding ',language, ' program at ', ctime() )

def music():
    for i in range(20):
      time.sleep(3)
      print('I\'m listening music at ', ctime())

if __name__ == '__main__':

    print('thread %s is running...' % threading.current_thread().name)

    thread_list = []
    t1 = threading.Thread(target=coding, args=('Python',))
    t2 = threading.Thread(target=music)
    thread_list.append(t1)
    thread_list.append(t2)
    t1.start()
    t2.start()

    # for t in thread_list:
    #     t.setDaemon(True)  # 设置为守护线程
    #     t.start()
    #     t.join()  # 在这个子线程完成运行之前，主线程将一直被阻塞

    print('thread %s ended.' % threading.current_thread().name)