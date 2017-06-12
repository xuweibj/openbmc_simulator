# Simulator for Test

Supported Arch: PPC64LE

Install and Start Simulator
---------------------------

* Clone this repo

* Run ``./simulator [-c] [-n <NIC> -r <IP range>]`` 

For Ubuntu OS, please run ``apt-get update`` first

Options
-------

**-c**: Cleanup IPs configuration. If not set it, will setup openbmc simulator environment and start simulator

**-n**: NIC name which want to configure IPs on

**-r**: IPs want to configure on NIC. The format is as '10.[1|{1.10}].[1|{1..200}].[1|{1..200}]'

Example:

Setup environment and Start simulator ``./simulator -n eth0 -r 10.1.1.{1..10}``

Clear environment: 

    # ./simulator -c -n eth0 -r 10.1.1.{1..10}

Node Definition in xCAT
-----------------------

If the node that simulator runs on as below:

    ip=10.0.0.1
    
You can define the node as below:

    mkdef simulator groups=all bmc=10.0.0.1 mgt=openbmc bmcusername=root bmcpassword=0penBmc

Run Command Against Simulator
-----------------------------

Take ``rpower`` command as example:

    # rpower simulator on
    simulator: on
    
