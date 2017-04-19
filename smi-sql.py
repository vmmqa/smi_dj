from optparse import OptionParser  
import sys
import os
import socket
import subprocess
#from subprocess import Popen, PIPE
#rc = subprocess.call(["ls","-l"])
#if __name__ == '__main__':
def main():
    ret=0#return code
    msg=str()#log info
    usage = "usage: %prog [-a | -d] entry"
    parser = OptionParser(usage=usage)
    parser.add_option("-a", "--add", type="string", dest="adder",  
                  help="please input the entry to add")
    parser.add_option("-i","--ip",type="string",dest="ipaddr",
                  help="please input the sever's ip",default="local")
    parser.add_option("-d","--del",type="string",dest="deler",
                  help="please input the entry to delete")
    (options, args) = parser.parse_args()
    if options.adder!=None:
        print('it is for adder action')
        cmd="python smi-cli.py -h"
        localcmd='staf '+options.ipaddr+' process start shell command '
        localcmd+=cmd
        localcmd+=' workdir /home/sky-nuc-libo1/repos/dji/ wait returnstdout STDERRTOSTDOUT RETURNSTDERR'
        print("localcmd=",localcmd)
        ret=subprocess.call(localcmd, shell=True)
        print('returncode=',ret)
        if ret==0:
            msg="pass to reigster"
        elif ret==49:
            msg="already exists"
        else:
            msg="fail to register"
    elif options.deler!=None:
        print('it is for deleter action')
        localcmd='staf '+options.ipaddr+' process start command '
        localcmd+='python parms smi-cli.py -h '
        localcmd+=' workdir /home/sky-nuc-libo1/repos/dji/ wait returnstdout STDERRTOSTDOUT RETURNSTDERR'
        print("localcmd=",localcmd)
        ret=subprocess.call(localcmd, shell=True)
        print('returncode=',ret)
        if ret==0:
            msg="pass to deleter"
        else:
            msg="fail to deleter"
    else:
        msg="it is unsupported command"
        ret=-1

    print(msg)
    return ret


if __name__ == '__main__':
    msg=main()
    print(msg)
