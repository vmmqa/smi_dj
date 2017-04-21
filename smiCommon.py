def cmdparse(entry):
    lentry=entry.split(';')
    if(len(lentry)):
        a=lentry[0]
        bl=a.split(':')
        if(bl[0]=='ip'):
            ret=bl[1]
        else:
            print('bad first item=',bl)
            ret=None
    else:
        print("bad entry")
        ret=None
    return ret 

	    
#if __name__ == '__main__':
#    entry='ip:192.168.79.2;boardinfo:234;user:xiaoming'
#    print('return value=',cmdparse(entry))


#file copy 
#staf $host_ip fs copy $opt "$host_file" todirectory "$target_path" tomachine $vm_ip
#command executor
#staf $vm_ip process start shell wait command "$target_cmd" returnstdout
#may use shell-style
#Goal: Execute the following shell-style command "grep 'Count = ' /tests/out | awk '{print $5}'" redirecting its standard output and standard error to /tests/awk.out.
# add a workload support, which could stop all workload at the same time
