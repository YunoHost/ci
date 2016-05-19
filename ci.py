import os
import sys
import vagrant
from contextlib import contextmanager
from urllib import urlretrieve

VAGRANTFILE_VERSION = "834e48942903e7c1069bbdae278888a078201bc3"

@contextmanager
def debug_message(first, second="done"):
    sys.stdout.write(first)
    sys.stdout.flush()
    yield
    sys.stdout.write(" ")
    sys.stdout.write(second)
    if not second.endswith("\n"):
        sys.stdout.write("\n")


def main():
    if not os.path.exists("Vagrantfile") or not os.path.exists(VAGRANTFILE_VERSION):
        with debug_message("Retreiving Vagrantfile ..."):
            urlretrieve("https://raw.githubusercontent.com/YunoHost/Vagrantfile/%s/Vagrantfile" % VAGRANTFILE_VERSION, "Vagrantfile")
            open(VAGRANTFILE_VERSION, "w").write("")

    v = vagrant.Vagrant()


if __name__ == '__main__':
    main()
