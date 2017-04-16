from optparse import OptionParser  
import sys
import os
import socket
import subprocess
#from subprocess import Popen, PIPE
#rc = subprocess.call(["ls","-l"])
if __name__ == '__main__':
    usage = "usage: %prog [-r|-u boardid] [-f] [-i server's ip]"
    parser = OptionParser(usage=usage)
    parser.add_option("-r", "--register", type="string", dest="register",  
                  help="format, ip:xxx;username:xxx;user:xxx")
    parser.add_option("-i","--ip",type="string",dest="ipaddr",
                  help="please input the sever's ip",default="local")
    parser.add_option("-u","--unregister",type="string",dest="unregister",
                  help="please input the entry")
    parser.add_option("-f", "--force",  
                  action="store_true", dest="force", default=False,  
                  help="force to unregister the HW on the server even if it is running")  
    (options, args) = parser.parse_args()
    print(options.register)
    print(options.ipaddr)
    print(options.unregister)
    print(options.force)
    ip=socket.gethostbyname(socket.gethostname())
    username=socket.gethostname()
    userpc=os.getlogin()
    entry=None
    print("ip=",ip,",username=",username,",userpc=",userpc)
    sys.exit()
    if options.register!=None:
		print('it is for register action')
		cmd=['staf',options.ipaddr,'respool','add','pool','dji','entry',options.register]
		#p=subprocess.Popen(['staf',options.ipaddr,'respool','add','pool','dji','entry',options.register])
		print("cmd=",cmd)
		p=subprocess.Popen(cmd)
		p.wait()
		print('returncode=',p.returncode)
		if p.returncode==0:
			print("pass to reigster\n")
		elif p.returncode==49:
			print("already exists\n")
		else:
			print("fail to register\n")
    elif options.unregister!=None:
		print('it is for unregister action')
		postcmd='CONFIRM'
		cmd=['staf',options.ipaddr,'respool','remove','pool','dji','entry',options.unregister, 'confirm']
		if options.force==True:
			cmd.append('FORCE')
		print("cmd=",cmd)
		p=subprocess.Popen(cmd)
		p.wait()
		print('returncode=',p.returncode)
		if p.returncode==0:
			print("pass to unreigster\n")
		elif p.returncode==48:
			print("it does NOT exist\n")
		elif p.returncode==4010:
			print(" A resource pool entry you specified to REMOVE is owned.Use the -f or --force option if you are sure that the correct\
			      entry is specficed")
		else:
			print("fail to unregister\n")
    else:
		print('it is unsupported command')


