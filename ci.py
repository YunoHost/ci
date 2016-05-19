import os
import sys
import json
import vagrant
from datetime import datetime
from urllib import urlretrieve, urlopen
from contextlib import contextmanager

from fabric.api import settings, sudo

from default_args import default_arguments_for_app


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
                sudo("apt-get update")
                sudo("apt-get upgrade -y")
                sudo("apt-get dist-upgrade -y")
                sudo("yunohost tools postinstall -d ynh.local -p ynh")
                sudo("yunohost user create johndoe -f John -l Doe -m john.doe@ynh.local -q 0 -p ynh")

        with debug_message("Halting vm to do a snapshot"):
            v.halt("testing")

        with debug_message("Saving a snapshot"):
            v.snapshot_save("postinstalled")

    if "postinstalled" not in v.snapshot_list():
        sys.stderr.write("Error: testing vm has already been created and I can't find a postinstalled snapshot, this is an inconsistante state, I don't know what to do, abort.\n")
        sys.stderr.write("You might want to run a vagrant destroy testing but be aware that this will DESTROY your modified vm.")
        sys.exit(1)

    with debug_message("Getting yunohost version"):
        v.snapshot_restore("postinstalled")
        with settings(host_string=v.user_hostname_port(vm_name="testing"),
                      key_filename=v.keyfile(vm_name="testing"),
                      disable_known_hosts=True):
            yunohost_version = json.loads(sudo("yunohost --version --output-as json"))

    app_list = json.load(urlopen("https://app.yunohost.org/official.json"))

    logs = {
        "yunohost_version": yunohost_version,
        "run_started_at": datetime.now().strftime("%F %X"),
        "apps": {}
    }

    for name, data in sorted(app_list.items(), key=lambda x: x[0]):
        with debug_message("Restoring snapshot"):
            v.snapshot_restore("postinstalled")

        with debug_message("Testing %s installation" % name):
            with settings(host_string=v.user_hostname_port(vm_name="testing"),
                          key_filename=v.keyfile(vm_name="testing"),
                          disable_known_hosts=True, ok_ret_codes=range(10000)):
                start = datetime.now()
                result = sudo("yunohost app install %s --verbose -a \"%s\"" % (name, default_arguments_for_app(data)))
                end = datetime.now()
                print "return code:", result.return_code

        logs["apps"][name] = {
            "output": result,
            "version": data["git"]["revision"],
            "return_code": result.return_code,
            "duration": (end - start).total_seconds(),
            "list.json_data": data,
        }

    logs["run_ended_at"] = datetime.now().strftime("%F %X")

    open("logs.json", "w").write(json.dumps(logs, indent=4))

if __name__ == '__main__':
    main()
