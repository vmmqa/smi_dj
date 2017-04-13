# Written by Libo
import smiCommon
import os
import sys
import subprocess
import multiprocessing
import time
import random
from optparse import OptionParser  
#==================
# input worker
def inputQ(queue,i):
    info = str(os.getpid()) + '(put):' + str(time.time()) +'(number):'+str(i)
    #print(info)
    queue.put(info)
def inputQ(queue,testplan,workload,ip, command):
    #currently two steps:
    #copy the testplan to remote machine specified dir
    #lanuch the common command on each ip
    #info = str(os.getpid()) + '(put):' + str(time.time()) +'(number):'+str(i)
    ##################################################
    #copy the testplan to remote machine specified dir
    ###################################################
    localcmd1='staf local fs copy file '+testplan
    localcmd1+=' todirectory '+workload+' tomachine '
    localcmd1+=ip
    print('localcmd1=',localcmd1)
    ret=subprocess.call(localcmd1, shell=True)
    if ret:
        output='fail to execute '+ localcmd1+' ret='+str(ret)
	print(output)
        queue.put(output)
	return
    else:
	print('pass to execute localcmd1')

    ########################################################
    #lanuch the common command on each ip and put into queue
    #######################################################
    localcmd2='staf ' +ip+' process start shell command '
    localcmd2+=command
    localcmd2+=' wait returnstdout'
    process=os.popen(localcmd2)
    print(localcmd2)
    tr=random.uniform(1,10) 
    print('tr=',tr)
    time.sleep(tr)
    output="the result of ("
    output+=ip
    output+=") and cmd=("
    output+=command
    output+=")"
    output+='\n'
    output+=process.read()
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
    optParser.add_option("-w","--workspace",action = "store",type="string",dest = "workspace",default="/home/sky-nuc-libo1/repos/dji/example/")
    optParser.add_option("-r","--run",action = "append",dest = "run")
    #fakeArgs = ['-f','file.txt','-v','good luck to you', 'arg2', 'arge','-f','file2.txt']
    #fakeArgs = ['-r','ip:192;broadinfo:xiaoming;user:xiaoming','-r','ip:193']  
    #options, args = optParser.parse_args(fakeArgs)
    options, args = optParser.parse_args()
    print(type(options.run),options.run)
    print(type(options.testplan),options.testplan)
    record1 = []   # store input processes
    record2 = []   # store output processes
    lock  = multiprocessing.Lock()    # To prevent messy print
    queue = multiprocessing.Queue(3)


    ipl = [] #store all the board ip
    for item in options.run:
        ipl.append(smiCommon.cmdparse(item))
    print(ipl)
    if(len(options.testplan)==0 or len(options.run)==0):
    	sys.exit()
    
    #dic = {'192.168.79.1':'service list', 'local':'var list','192.168.79.2':'help help'}
    #dic = {'10.239.196.96':'calc', 'local':'ls -l','10.239.159.58':'sleep 10s'}
    cmd="sleep 2s"
    # input processes
    #for key in dic:
        #process = multiprocessing.Process(target=inputQ,args=(queue,i))
    for ip in ipl:
        process = multiprocessing.Process(target=inputQ,args=(queue,options.testplan,options.workspace,ip,cmd))
        process.start()
        record1.append(process)

    # output processes
    #for key in dic:
    for ip in ipl:
        process = multiprocessing.Process(target=outputQ,args=(queue,lock))
        process.start()
        record2.append(process)

    for p in record1:
        p.join()

    queue.close()  # No more object will come, close the queue

    for p in record2:
        p.join()

    print("all process finishs!")

