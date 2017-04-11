from optparse import OptionParser  
if __name__ == '__main__':
    usage = "myprog[ -f <filename>][-s <xyz>] arg1[,arg2..]"
    optParser = OptionParser(usage)
    optParser.add_option("-f","--file",action = "store",type="string",dest = "fileName")
    optParser.add_option("-r","--run",action = "append",dest = "run")
    optParser.add_option("-v","--vison", action="store_false", dest="verbose",default='None',
                     help="make lots of noise [default]")   
    #fakeArgs = ['-f','file.txt','-v','good luck to you', 'arg2', 'arge','-f','file2.txt']
    fakeArgs = ['-r','ip:192;broadinfo:xiaoming;user:xiaoming','-r','ip:193']  
    options, args = optParser.parse_args(fakeArgs)
    print (options.fileName)
    print (options.verbose)
    print ("options=",options)
    print ("args=",args)
    print (optParser.print_help())
    print(type(options.run),options.run)
