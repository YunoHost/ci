# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

  # Default folder sharing
  config.vm.synced_folder ".", "/vagrant"
  # Force guest type, because YunoHost /etc/issue can't be tuned
  config.vm.guest = :debian

  config.vm.define "stretch-unstable" do |stretch_unstable|
    stretch_unstable.vm.box = "yunohost/stretch-unstable"
    stretch_unstable.vm.box_url = "https://build.yunohost.org/yunohost-stretch-unstable.box"
    stretch_unstable.vm.network :private_network, ip: "192.168.33.83"
  end

end
