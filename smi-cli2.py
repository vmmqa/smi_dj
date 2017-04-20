from optparse import OptionParser  
import sys
import os
import socket
import getpass
import subprocess
#from subprocess import Popen, PIPE
#rc = subprocess.call(["ls","-l"])
#if __name__ == '__main__':
def main():
    ret=0#return code
    msg=str()#log info
    usage = "usage: %prog [-r|-u boardid] [-f] [-i server's ip]"
    parser = OptionParser(usage=usage)
    parser.add_option("-r", "--register", type="string", dest="register",  
                  help="format, board")
    parser.add_option("-i","--ip",type="string",dest="ipaddr",
                  help="please input the sever's ip",default="local")
    parser.add_option("-u","--unregister",type="string",dest="unregister",
                  help="please input the entry")
    parser.add_option("-f", "--force",  
                  action="store_true", dest="force", default=False,  
                  help="force to unregister the HW on the server even if it is running")  
    (options, args) = parser.parse_args()
    print("register=%s,ipaddr=%s,unregister=%s,force=%d"%(options.register,options.ipaddr,options.unregister,options.force))
    ipList=socket.gethostbyname_ex(socket.gethostname())
    username=getpass.getuser()
    userpc=socket.gethostname()
    entry=str()
    ip=str()
    ipMask="10.9" #which indicates it is the specified subnet
    for i in ipList[2]:
        if i.find(ipMask) !=-1:
            ip=i
    print("ClientIP=%s, UserName=%s,UserPC=%s"%(ip,username,userpc))
    if(len(ip) and len(username) and len(userpc) and ip.find(ipMask)==0):
        entry+="ClientIP:"
        entry+=ip
        entry+=",UserName:"
        entry+=username
        entry+=",UserPC:"
        entry+=userpc
        print("entry=",entry)
    else:
        parser.print_help()
        print("Error, the username, userpc and ip can't be blank and the ip should start from %s"%ipMask)
        return -1
    if options.register!=None:
        print('it is for register action')
        entry+=",DeviceID:"
        entry+=options.register
        localcmd1=['staf',options.ipaddr,'respool','add','pool','dji','entry',entry]
		#p=subprocess.Popen(['staf',options.ipaddr,'respool','add','pool','dji','entry',options.register])
        print("localcmd1=%s"%localcmd1)
        p=subprocess.Popen(localcmd1)
        p.wait()
        ret=p.returncode
        print('returncode=%d'%p.returncode)
        if p.returncode==0:
            msg="pass to reigster"
            localcmd2='staf '+options.ipaddr
            localcmd2+=' process start shell wait command python smi-sql.py -a '
            localcmd2+=entry
            localcmd2+=" workdir /home/dji/xmzhang/0419/MysqlWrapper"
            print('localcmd2=%s'%localcmd2)
            ret=subprocess.call(localcmd2, shell=True)
            if ret:
                output='fail to execute '+ localcmd2+' ret='+str(ret)
                print(output)
                return -2
            else:
                print('pass to execute broad sql register')
        elif p.returncode==49:
            msg="already exists"
        else:
            msg="fail to register"
    elif options.unregister!=None:
        print('it is for unregister action')
        postcmd='CONFIRM'
        entry+=",DeviceID:"
        entry+=options.unregister
        localcmd1=['staf',options.ipaddr,'respool','remove','pool','dji','entry',entry, 'confirm']
        if options.force==True:
            cmd.append('FORCE')
        print("localcmd1=%s"%localcmd1)
        p=subprocess.Popen(localcmd1)
        p.wait()
        ret=p.returncode
        print('returncode=%d'%p.returncode)
        if p.returncode==0:
            msg="pass to unreigster"
            localcmd2='staf '+options.ipaddr
            localcmd2+=' process start shell wait command python smi-sql.py -d '
            localcmd2+=entry
            localcmd2+=" workdir /home/dji/xmzhang/0419/MysqlWrapper"
            print('localcmd2=%s'%localcmd2)
            ret=subprocess.call(localcmd2, shell=True)
            if ret:
                output='fail to execute '+ localcmd2+' ret='+str(ret)
                print(output)
                return -2
            else:
                print('pass to execute broad sql delete')
        elif p.returncode==48:
            msg="it does NOT exist"
        elif p.returncode==4010:
            msg=" A resource pool entry you specified to REMOVE is owned.Use the -f or --force option if you are sure that the correct\
                entry is specficed"
        else:
            msg="fail to unregister"
    else:
        msg="it is unsupported command"
        ret=-1

    print(msg)
    return ret


if __name__ == '__main__':
    ret=main()
    print("the return value=%d"%ret)
