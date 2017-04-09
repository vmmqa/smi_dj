# smi_dj
Getting started
===============

smi stands for System Management Interface, it is used for distributed system based on
one opensource tool staf(Software Testing Automation Framework) To get started, [check out the installation
instructions in the
documentation](http://staf.sourceforge.net/).

this framework could be divided into two parts: Client and Server

Client started
===============

1. install the staf and the smi-cli.py file
2. add below statement into <STAFDIR>/bin/STAF.cfg file
  trust level 5 default
3. lanuch staf by invoking startSTAFProcess.sh(Linux)
4. run smi_cli.py to register/unregister resource to sever. the usage of this script could be got by:
  python smi-cli.py -h

bear in mind, the verified version of python is  on 3.4 and 2.7.


Server started
===============
1. install the staf and the smi-server.py file
2. add below statement into <STAFDIR>/bin/STAF.cfg file
  trust level 4 default
  SERVICE respool LIBRARY STAFPool
3. lanuch staf by invoking startSTAFProcess.sh(Linux)
4. create one resource pool which is the common place to put all the resources by below command only ONCE,
  the dji is the pool name:
  staf local respool create pool dji description "example project" 

Now this framework has been setup. :) bear in mind, this server could be ONLY used by administraction which could do control all the registered resources.
