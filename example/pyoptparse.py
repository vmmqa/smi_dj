from optparse import OptionParser  
if __name__ == '__main__':
    parser = OptionParser()  
    parser.add_option("-f", "--file", dest="filename",  
                  help="test report", metavar="FILE")
    parser.add_option("-i","--ip",type="string",dest="ipaddr",
                  help="please input the sever's ip",default="local")
    parser.add_option("-c","--command",type="string",dest="cmd",
                  help="please input the triggerred command",default="list")
    parser.add_option("-q", "--quiet",  
                  action="store_false", dest="verbose", default=True,  
                  help="don't print status messages to stdout")  
  
    (options, args) = parser.parse_args()
    print(options.ipaddr)
    print(options.cmd)
    #currently it only supports commands: list/launch

    if options.cmd=='list':
        print('it is for list action')
    elif options.cmd=='launch':
        print('it is for launch action')
    else:
        print('it is unsupported command')

    #todo: 1. -l,--list; 2. -c (lanuch entry;entry;entry)
