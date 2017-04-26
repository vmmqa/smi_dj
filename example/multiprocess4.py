from multiprocessing import Process, Lock
import time 

def f(l, i):
    l.acquire()
    try:
        print('hello world', i)
        time.sleep(1)
    finally:
        l.release()

if __name__ == '__main__':
    lock = Lock()

    for num in range(10):
        p=Process(target=f,args=(lock,num))
        p.start()
        print(p.is_alive())
        print(p.name)

