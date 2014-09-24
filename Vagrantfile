# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
    # Note that some VMs have dependencies to other dito. Take this into account when ordering the VM entries.
    config.vm.define "gadget" do |gadget|

        # Gadget
        # ======
        # Postgres
        # RabbitMQ
        # redis

        gadget.vm.box = "ubuntu/trusty64"
        gadget.vm.hostname = "gadget"
        gadget.vm.network "private_network", ip: "10.0.10.12"

        gadget.vm.provision :shell, path: "scripts/postgres.p.sh", privileged: true
        gadget.vm.provision :shell, path: "scripts/postgres.dev.p.sh", privileged: true
        gadget.vm.provision :shell, path: "scripts/postgres.sentry.dev.u.sh", privileged: false

        gadget.vm.provision :shell, path: "scripts/rabbitmq.p.sh", privileged: true
        gadget.vm.provision :shell, path: "scripts/redis.p.sh", privileged: true
        gadget.vm.provision :shell, path: "scripts/redis.dev.p.sh", privileged: true
    end

    config.vm.define "dale" do |dale|

        # Dale
        # ====
        # Sentry
        #
        # Depends on
        # ----------
        # Gadget (for DB)

        dale.vm.box = "ubuntu/trusty64"
        dale.vm.hostname = "dale"
        dale.vm.network "private_network", ip: "10.0.10.11"

        dale.vm.provision :shell, path: "scripts/python.p.sh", privileged: true
        dale.vm.provision :shell, path: "scripts/python.virtualenv.u.sh", privileged: false

        dale.vm.provision :shell, path: "scripts/supervisor.p.sh", privileged: true
        dale.vm.provision :shell, path: "scripts/memcached.p.sh", privileged: true

        dale.vm.provision :shell, path: "scripts/sentry.dev.u.sh", privileged: false
    end

    config.vm.define "chip" do |chip|

        # Chip
        # ====
        # Django apps
        #
        # Depends on
        # ----------
        # Gadget (for DB)
        # Dale (for Sentry)

        chip.vm.box = "ubuntu/trusty64"
        chip.vm.hostname = "chip"
        chip.vm.network "private_network", ip: "10.0.10.10"

        chip.vm.provision :shell, path: "scripts/python.p.sh", privileged: true
        chip.vm.provision :shell, path: "scripts/python.virtualenv.u.sh", privileged: false

        chip.vm.provision :shell, path: "scripts/supervisor.p.sh", privileged: true
        chip.vm.provision :shell, path: "scripts/memcached.p.sh", privileged: true
    end

    config.vm.define "zipper" do |zipper|

        # Zipper
        # ======
        # Web endpoint
        #
        # Depends on
        # ----------
        # Chip (for something to proxy)
        # Dale (for something to proxy)

        zipper.vm.box = "ubuntu/trusty64"
        zipper.vm.hostname = "zipper"
        zipper.vm.network "private_network", ip: "10.0.10.13"
    end

    # Run on every machine
    config.vm.provision :shell, path: "scripts/hosts.dev.p.sh", privileged: true
end
