import os
import vagrant
from urllib import urlretrieve

VAGRANTFILE_VERSION = "834e48942903e7c1069bbdae278888a078201bc3"


def main():
    if not os.path.exists("vagrantfile"):
        urlretrieve("https://raw.githubusercontent.com/YunoHost/Vagrantfile/%s/Vagrantfile" % VAGRANTFILE_VERSION, "Vagrantfile")

    v = vagrant.Vagrant()


if __name__ == '__main__':
    main()
