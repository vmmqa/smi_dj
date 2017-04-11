# Written by Libo
import os
import sys
import multiprocessing
import time
from optparse import OptionParser  
#==================
# input worker
def inputQ(queue,i):
    info = str(os.getpid()) + '(put):' + str(time.time()) +'(number):'+str(i)
    #print(info)
    queue.put(info)
def inputQ(queue,key, command):
    #info = str(os.getpid()) + '(put):' + str(time.time()) +'(number):'+str(i)
    #print(info)
    localcmd='staf '+key+' '+command
    process=os.popen(localcmd)
    print(localcmd)
    output=process.read()
    process.close()
    queue.put(output)
    
# output worker
def outputQ(queue,lock):
    info = queue.get()
    lock.acquire()
    print (str(os.getpid()) + '(get):' + info)
    lock.release()
#===================
# Main
if __name__ == '__main__':
    optParser = OptionParser()
    optParser.add_option("-t","--testplan",action = "store",type="string",dest = "testplan")
    optParser.add_option("-r","--run",action = "append",dest = "run")
    #fakeArgs = ['-f','file.txt','-v','good luck to you', 'arg2', 'arge','-f','file2.txt']
    #fakeArgs = ['-r','ip:192;broadinfo:xiaoming;user:xiaoming','-r','ip:193']  
    #options, args = optParser.parse_args(fakeArgs)
    options, args = optParser.parse_args()
    print(type(options.run),options.run)
    sys.exit()
    record1 = []   # store input processes
    record2 = []   # store output processes
    lock  = multiprocessing.Lock()    # To prevent messy print
    queue = multiprocessing.Queue(3)
    dic = {'192.168.79.1':'service list', 'local':'var list','192.168.79.2':'help help'}

    # input processes
    #for i in range(10):
    for key in dic:
        #process = multiprocessing.Process(target=inputQ,args=(queue,i))
        process = multiprocessing.Process(target=inputQ,args=(queue,key,dic[key]))
        process.start()
        record1.append(process)

    # output processes
    #for i in range(10):
    for key in dic:
        process = multiprocessing.Process(target=outputQ,args=(queue,lock))
        process.start()
        record2.append(process)

    for p in record1:
        p.join()

    queue.close()  # No more object will come, close the queue

    for p in record2:
        p.join()

    print("all process finishs!")

