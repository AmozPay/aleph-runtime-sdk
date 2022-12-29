# The runtime init steps

## init0.sh

The first program executed is `/sbin/init`, which you can find [here](/runtimes/aleph-debian-11-python-base).

It does the following, in order:
- mounts the filesystems,
- creates an ssh server,
- calls an optional setup script `/root/init0_plugin.sh`
- executes `/root/init1.py`

You can create your optional setup script:

```bash
cat << EOT > init0_plugin.sh
#!/bin/sh
echo "Hello World!"
EOT

```

## init1.py

The program `/root/init1.py` does the following steps, in order:

- opens sockets for communication
- sets up hostname
- load environment variables
- attach storage volumes
- sets up network
- sets up user code
- calls user code with payload
- sends response
- waits a bit and repeats the 2 previous steps until the lamda function is not called for a while
- does some cleanup steps
- shuts down


To customize the behavior of `init1.py`, you can create plugins in `/root/custom_plugins.py`

To do so, follow [this tutorial](./2-plugins.md)
