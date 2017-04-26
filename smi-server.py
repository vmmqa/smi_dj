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
def cmdparseMap(entry):
    lentry=entry.split(',')
    cmdLen=len(lentry)
    dictEntry={}
    while(cmdLen):
        cmdLen=cmdLen-1
        key=lentry[cmdLen].split(':')[0]
        value=lentry[cmdLen].split(':')[1]
        dictEntry[key]=value
    return dictEntry

def sqlAction(command):
    localCommand="python MysqlWrapper/smi-sql.py "
    localCommand+=command
    ret=subprocess.call(localCommand,shell=True)
    if ret==0:
        print("pass to execute %s"%command)
    else:
        print("Fail to execute %s"%command)
    return ret

# input worker
def inputQ(queue,i):
    info = str(os.getpid()) + '(put):' + str(time.time()) +'(number):'+str(i)
    #print(info)
    queue.put(info)
def inputQ(queue,testplan,workspace,item, command):
    #currently two steps:
    #copy the testplan to remote machine specified dir
    #lanuch the common command on each ip
    #info = str(os.getpid()) + '(put):' + str(time.time()) +'(number):'+str(i)
    entryDict=cmdparseMap(item)
    ip=entryDict["ClientIP"]
    deviceID=entryDict["DeviceID"]
    print("ip=%s,deviceID=%s"%(ip,deviceID))
    ##################################################
    #create and copy the testplan to remote machine specified dir
    ###################################################
    cmdstep1='staf '+ip+' fs create directory '
    cmdstep1+=workspace+deviceID
    print('cmdstep1=',cmdstep1)
    ret=subprocess.call(cmdstep1, shell=True)
    if ret:
        output='fail to execute '+ cmdstep1+' ret='+str(ret)
        print(output)
        queue.put(output)
        return
    else:
	    print('pass to execute cmdstep1')

    cmdstep2='staf local fs copy file '+testplan
    cmdstep2+=' todirectory '+workspace+deviceID+' tomachine '
    cmdstep2+=ip
    print('cmdstep2=',cmdstep2)
    ret=subprocess.call(cmdstep2, shell=True)
    if ret:
        output='fail to execute '+ cmdstep2+' ret='+str(ret)
        print(output)
        queue.put(output)
        return
    else:
	    print('pass to execute cmdstep2')

    ########################################################
    #lanuch the common command on each ip and put into queue
    #######################################################
    cmdstep3='staf ' +ip+' process start shell command '
    cmdstep3+=command
    cmdstep3+=' wait returnstdout'
    #process=os.popen(cmdstep3)
    print(cmdstep3)
    #tr=random.uniform(1,10) 
    #print('tr=',tr)
    #time.sleep(tr)

    preCommand=" "+item
    preCommand+=" -u status:running"
    if(sqlAction(preCommand)==0):
        print("pass to update running status")
    else:
        return
    ret=subprocess.call(cmdstep3,shell=True)
    #output="the result of ("
    #output+=item
    #output+=") and cmd=("
    #output+=command
    #output+=")"
    #output+=str(ret)
    #output+='\n'
        
    output=" "+item
    output+=" -u status:"
    if ret==0:
        output+="pass"
    else:
        output+="fail"
  #  output+=process.read()
 #   process.close()
#    ret=process.exitcode
    print("item=%s,ret=%d\n"%(item,ret))
    queue.put(output)
    if(sqlAction(output)==0):
        print("pass to update pass/fail status")
    else:
        return
    
# output worker
def outputQ(queue,lock):
    info = queue.get()
    lock.acquire()
    print (str(os.getpid()) + '(get):' + info)
    #update the sql
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


    #ipl = [] #store all the board ip
    #for item in options.run:
    #    ipl.append(smiCommon.cmdparse(item))
   # print(ipl)
    if(len(options.testplan)==0 or len(options.run)==0):
    	sys.exit()
    
    #dic = {'192.168.79.1':'service list', 'local':'var list','192.168.79.2':'help help'}
    #dic = {'10.239.196.96':'calc', 'local':'ls -l','10.239.159.58':'sleep 10s'}
    cmd="sleep 2s"
    # input processes
    #for key in dic:
        #process = multiprocessing.Process(target=inputQ,args=(queue,i))
    for item in options.run:
        process = multiprocessing.Process(target=inputQ,args=(queue,options.testplan,options.workspace,item,cmd))
        process.start()
        record1.append(process)

    # output processes
    #for key in dic:
    for item in options.run:
        process = multiprocessing.Process(target=outputQ,args=(queue,lock))
        process.start()
        record2.append(process)

    for p in record1:
        p.join()

    queue.close()  # No more object will come, close the queue

    for p in record2:
        p.join()

    print("all process finishs!")

