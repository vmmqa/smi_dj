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

1. install the staf and the smi_cli.py file
2. add below statement into <STAFDIR>/bin/STAF.cfg file
  trust level 5 default
3. run smi_cli.py to register/unregister resource to sever. the usage of this script could be got by:
  python smi_cli.py -h

bear in mind, the verified version of python is  on 3.4 and 2.7.
