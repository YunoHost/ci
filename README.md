Prototype of continuous integration for YunoHost using vagrant.

For now this:

* create a vagrant box with YunoHost unstable
* update/dist-upgrade
* add a default user
* then at this point it creates a snapshot of the vm
* all of the previous is only done once
* then it runs all tests

To run you'll probably need the latest version of Vagrant which is just a self containted .deb to install (works on ubuntu and is targeted for debian).

Debian packages:

    sudo apt-get install python-dev gcc python-virtualenv

Create your python virtualenv:

    virtualenv ve
    source ve/bin/activate
    pip install -r requirements.txt

To run (expect this to be long):

    python ci_core.py
