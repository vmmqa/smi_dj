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
#parse the entry into dict format
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

#==================================
#mySQL wrapper. it will execute subdir smi-sql.py
#details usage refer to it
def sqlAction(command):
    localCommand="python MysqlWrapper/smi-sql.py "
    localCommand+=command
    ret=subprocess.call(localCommand,shell=True)
    if ret==0:
        print("pass to execute %s"%command)
    else:
        print("Fail to execute %s"%command)
    return ret

#===================================
#use mutliprocess to lanuch multi jobs at the same time
#the workspace is one for client
#the item is the register entry
#the command is the invoked wrapper script on client to lanuch job
#the duration is the timeout for each job
def inputQ(queue,testplan,workspace,item, command,duration):
    #currently two steps:
    #copy the testplan to remote machine specified dir
    #lanuch the common command on each ip
    #info = str(os.getpid()) + '(put):' + str(time.time()) +'(number):'+str(i)
    entryDict=cmdparseMap(item)
    ip=entryDict["ClientIP"]
    deviceID=entryDict["DeviceID"]
    command+=deviceID

    timestamp = strftime("%Y-%m-%d_%H-%M-%S", localtime())
    command+=" "+timestamp
    print("ip=%s,deviceID=%s,command=%s,duration=%s"%(ip,deviceID,command,duration))
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

    ltestplan=testplan.split('/')
    testplanName=ltestplan(len(ltestplan)-1)
    preCommand=" "+item
    preCommand+=" -u PlanName:"+testplanName
    if(sqlAction(preCommand)==0):
        print("pass to update PlanName value")
    else:
        print("fail to update PlanName value")
        return

    ########################################################
    #lanuch the common command on each ip and put into queue
    #######################################################
    cmdstep3='staf ' +ip+' process start shell command "'
    cmdstep3+=command
    cmdstep3+='" wait '+duration
    cmdstep3+='  returnstdout stderrtostdout returnstderr'
    #process=os.popen(cmdstep3)
    print(cmdstep3)
    #tr=random.uniform(1,10) 
    #print('tr=',tr)
    #time.sleep(tr)

    preCommand=" "+item
    preCommand+=" -u DeviceStatus:busy,JobStatus:running,JobStartTime:"

    preCommand+=timestamp
    if(sqlAction(preCommand)==0):
        print("pass to update running status")
    else:
        return
    ret=subprocess.call(cmdstep3,shell=True)
        
    output=" "+item
    output+=" -u DeviceStatus:free,JobStatus:"
    if ret==0:
        output+="pass"
    else:
        output+="fail"
    print("item=%s,ret=%d\n"%(item,ret))
    queue.put(output)
    if(sqlAction(output)==0):
        print("pass to update pass/fail status")
    else:
        return

#===========================================
# output worker
#it reap all the lanuch queue
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
    optParser.add_option("-d","--duration",action = "store",type="string",dest = "duration",default="1d",help="timeout for the longest test")
    optParser.add_option("-w","--workspace",action = "store",type="string",dest = "workspace",default=r'D:\\ATF_Cloud_WorkSpace\\ATF_Client\\config\\')
    optParser.add_option("-r","--run",action = "append",dest = "run")
    optParser.add_option("-f", "--flush", action="store_true", dest="flush",default=False,help="flush the registered entries status before lanuching jobs")
    #fakeArgs = ['-f','file.txt','-v','good luck to you', 'arg2', 'arge','-f','file2.txt']
    #options, args = optParser.parse_args(fakeArgs)
    options, args = optParser.parse_args()
    print(type(options.testplan),options.testplan)
    print(type(options.duration),options.duration)
    print(type(options.workspace),options.workspace)
    print(type(options.run),options.run)
    print(type(options.flush),options.flush)
    record1 = []   # store input processes
    record2 = []   # store output processes
    lock  = multiprocessing.Lock()    # To prevent messy print
    queue = multiprocessing.Queue(30) # could lanuch 30 jobs at the same time


    
    if(options.flush==True):
        print("flush all the status of registered entries")
        flushCmd=" staf local respool query pool dji | grep Entry: | awk '{print $2}' | uniq"
        process=os.popen(flushCmd)
        output=process.read()
        loutput=output.split('\n')
        print(type(loutput),loutput)
        for item in loutput[0:-1]:
            entryDict=cmdparseMap(item)
            ip=entryDict["ClientIP"]
            pingCmd='staf '+ip+' ping ping '
            print('pingCmd=%s'%pingCmd)
            sqlCommand=" " +item +" -u DeviceStatus:"
            ret=subprocess.call(pingCmd, shell=True)
            if ret:
                sqlCommand+="offline"
                print("the %s offline"%ip)
            else:
                sqlCommand+="online"
                print("the %s online"%ip)
            
            if(sqlAction(sqlCommand)==0):
                print("pass to update DeviceStatus value")
            else:
                print("fail to update DeviceStatus value")
            
        print("the output=%s"%output)
        sys.exit(0)

    elif(len(options.testplan)==0 or len(options.run)==0):
        sys.exit(1)
    else:            
        cmd=r'pushed D:\\ATF_Cloud_WorkSpace\\ATF_Client\\ && python ATF_Main.py '

        # input processes
        for item in options.run:
            process = multiprocessing.Process(target=inputQ,args=(queue,options.testplan,options.workspace,item,cmd))
            process.start()
            record1.append(process)

        # output processes
        for item in options.run:
            process = multiprocessing.Process(target=outputQ,args=(queue,lock))
            process.start()
            record2.append(process)
    
        #wait for the input Q to finish, default 1d
        for p in record1:
            p.join(86400)

        queue.close()  # No more object will come, close the queue

        #wait for the output Q to finish
        for p in record2:
            p.join(86400)

        print("all process finishs!")
        sys.exit(0)

