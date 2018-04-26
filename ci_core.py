import os
import sys
import json
import vagrant
import traceback
from contextlib import contextmanager

from fabric.api import settings, sudo


VAGRANTFILE_VERSION = "88ff9f40f30c132bfb482c057050f5bdcf37d379"

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
    v = vagrant.Vagrant()

    if "vagrant-vbguest" not in {x.name for x in v.plugin_list()}:
        os.system("vagrant plugin install vagrant-vbguest")

    starting_state = v.status("unstable")[0].state

    if starting_state == "not_created":
        with debug_message("Unstable vm not created, vagrant up-ing it"):
            v.up(vm_name="unstable")

        with debug_message("unstable vm created for the first time, starting postinstall"):
            with settings(host_string=v.user_hostname_port(vm_name="unstable"),
                          key_filename=v.keyfile(vm_name="unstable"),
                          disable_known_hosts=True):
                sudo("apt-get update")
                sudo("DEBIAN_FRONTEND='noninteractive' apt-get -y -o Dpkg::Options::='--force-confdef' -o Dpkg::Options::='--force-confold' dist-upgrade -qq")
                sudo("yunohost tools postinstall -d ynh.local -p ynh")
                sudo("yunohost user create johndoe -f John -l Doe -m john.doe@ynh.local -q 0 -p ynh --admin-password ynh")

        with debug_message("Halting vm to do a snapshot"):
            v.halt("unstable")

        with debug_message("Saving a snapshot"):
            v.snapshot_save("unstable", "postinstalled")

    if "postinstalled" not in v.snapshot_list():
        sys.stderr.write("Error: unstable vm has already been created and I can't find a postinstalled snapshot, this is an inconsistante state, I don't know what to do, abort.\n")
        sys.stderr.write("You might want to run a vagrant destroy unstable but be aware that this will DESTROY your modified vm.")
        sys.exit(1)

    with debug_message("Getting yunohost version"):
        v.snapshot_restore("unstable", "postinstalled")
        with settings(host_string=v.user_hostname_port(vm_name="unstable"),
                      key_filename=v.keyfile(vm_name="unstable"),
                      disable_known_hosts=True):
            yunohost_version = json.loads(sudo("yunohost --version --output-as json"))


    for test in os.listdir("tests"):
        # only handle test_*.py files
        if not test.endswith(".py") or not test.startswith("test_"):
            continue

        # quote from doc
        # When importing a module from a package, note that __import__('A.B', ...)
        # returns package A when fromlist is empty, but its submodule B when
        # fromlist is not empty.
        # so we put garbage in fromlist to have this behavior
        test = __import__("tests.%s" % test[:-len(".py")], fromlist=["a"])

        for test_function in dir(test):
            if not test_function.startswith("test_"):
                continue

            v.snapshot_restore("unstable", "postinstalled")
            sys.stdout.write("%s.%s...\r" % (test.__name__, test_function))
            sys.stdout.flush()
            try:
                getattr(test, test_function)()
            except Exception as e:
                sys.stdout.write("FAILED\n")
                traceback.print_exc()
                print e
            else:
                sys.stdout.write("SUCESS\n")


if __name__ == '__main__':
    main()
