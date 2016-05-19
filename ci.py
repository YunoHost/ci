import os
import sys
import vagrant
from urllib import urlretrieve

VAGRANTFILE_VERSION = "834e48942903e7c1069bbdae278888a078201bc3"


def main():
    if not os.path.exists("Vagrantfile") or not os.path.exists(VAGRANTFILE_VERSION):
        sys.stdout.write("Retreiving Vagrantfile ...")
        sys.stdout.flush()
        urlretrieve("https://raw.githubusercontent.com/YunoHost/Vagrantfile/%s/Vagrantfile" % VAGRANTFILE_VERSION, "Vagrantfile")
        open(VAGRANTFILE_VERSION, "w").write("")
        sys.stdout.write(" done\n")

    v = vagrant.Vagrant()


if __name__ == '__main__':
    main()
