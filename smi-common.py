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


