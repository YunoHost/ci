Prototype of continuous integration for YunoHost using vagrant.

For now this:

* create a default vagrant box with YunoHost 2.4 using opi's box
* update/upgrade/dist-upgrade
* add a default user
* then at this point it creates a snapshot of the vm
* all of the previous is only done once
* then, for all YunoHost official apps it will: restart from the snapshot, try to install the app, log the output and do the same for the next app
* logs everything in a logs.json file for further uses (like a nice dashboard :p)

To run you'll probably need the latest version of Vagrant which is just a self containted .deb to install (works on ubuntu and is targeted for debian).

For amd64:

    wget https://releases.hashicorp.com/vagrant/1.8.1/vagrant_1.8.1_x86_64.deb
    sudo dpkg -i vagrant_1.8.1_i686.rpm

    # or

    wget https://releases.hashicorp.com/vagrant/1.8.1/vagrant_1.8.1_i686.deb
    sudo dpkg -i vagrant_1.8.1_i686.deb


Create your python virtualenv:

    virtualenv ve
    source ve/bin/activate
    pip install -r requirements.txt

To run (expect this to be long):

    python ci.py

It creates a `logs.json` with every information needed to reuse the outputed data.
