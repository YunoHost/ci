import os
import sys
import json
import vagrant
from urllib import urlretrieve, urlopen
from contextlib import contextmanager

from fabric.api import settings, run

VAGRANTFILE_VERSION = "834e48942903e7c1069bbdae278888a078201bc3"

@contextmanager
def debug_message(first, second="done"):
    sys.stdout.write(first)
    sys.stdout.write(" ...\r")
    sys.stdout.flush()
    yield
    sys.stdout.write("%s ... %s" % (first, second))
    if not second.endswith("\n"):
        sys.stdout.write("\n")


def main():
    if not os.path.exists("Vagrantfile") or not os.path.exists(VAGRANTFILE_VERSION):
        with debug_message("Retreiving Vagrantfile"):
            urlretrieve("https://raw.githubusercontent.com/YunoHost/Vagrantfile/%s/Vagrantfile" % VAGRANTFILE_VERSION, "Vagrantfile")
            open(VAGRANTFILE_VERSION, "w").write("")

    v = vagrant.Vagrant()

    starting_state = v.status("testing")[0].state

    if starting_state == "not_created":
        with debug_message("Testing vm not created, vagrant up-ing it"):
            v.up(vm_name="testing")

        with debug_message("Testing vm created for the first time, starting postinstall"):
            with settings(host_string=v.user_hostname_port(vm_name="testing"),
                          key_filename=v.keyfile(vm_name="testing"),
                          disable_known_hosts=True):
                run("sudo yunohost tools postinstall -d ynh.local -p ynh")

        with debug_message("Halting vm to do a snapshot"):
            v.halt("testing")

        with debug_message("Saving a snapshot"):
            v.snapshot_save("postinstalled")

    if "postinstalled" not in v.snapshot_list():
        sys.stderr.write("Error: testing vm has already been created and I can't find a postinstalled snapshot, this is an inconsistante state, I don't know what to do, abort.")
        sys.exit(1)

    if starting_state == "running":
        with debug_message("Halting the testing vm before starting to work"):
            v.halt("testing")

    app_list = json.load(urlopen("https://app.yunohost.org/official.json"))



if __name__ == '__main__':
    main()
