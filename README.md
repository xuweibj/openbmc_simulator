# Simulator for Test

Supported Arch: PPC64LE

Install and Start Simulator
---------------------------

* Clone this repo

* Run ``./simulator``

For Ubuntu OS, please run ``apt-get update`` first

Node Definition
---------------

If the node that simulator runs on as below:

    ip=10.0.0.1
    
You can define the node as below:

    mkdef simulator groups=all bmc=10.0.0.1 mgt=openbmc bmcusername=root bmcpassword=0penBmc

Run Command Against Simulator
-----------------------------

Take ``rpower`` command as example:

    # rpower simulator on
    simulator: on
    
