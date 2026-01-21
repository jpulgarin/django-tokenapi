# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
  config.vm.synced_folder ".", "/vagrant"
  config.vm.define "tokenapi", primary: true do |tokenapi|
    tokenapi.vm.box = "bento/debian-11.7"
    tokenapi.vm.hostname = "tokenapi"

    tokenapi.vm.provider "virtualbox" do |vb|
      vb.memory = "2048"
    end

    tokenapi.vm.provision "shell", inline: <<-SHELL
      apt-get update
      DEBIAN_FRONTEND="noninteractive" apt-get install -y build-essential python3-venv
    SHELL

    tokenapi.vm.provision "create-virtualenv-py3", type: :shell, privileged: false, inline: <<-SHELL
      cd ~
      python3 -m venv venv_py3
    SHELL

    tokenapi.vm.provision "pip3-install", type: :shell, privileged: false, inline: <<-SHELL
      source ~/venv_py3/bin/activate
      pip3 install django==4.0.10 six
    SHELL

    tokenapi.vm.provision "bashrc", type: :shell, privileged: false, inline: <<-SHELL
      echo "cd /vagrant" >> ~/.bashrc
      echo "source ~/venv_py3/bin/activate" >> ~/.bashrc
    SHELL
  end
end

