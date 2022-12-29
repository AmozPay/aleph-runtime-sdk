# Define your runtime filesystem

During the runtime build:

- packages can be added/removed
- additional static setup can be done
- plugins can be added

In fact, it is quite simple to do, since it is based on Dockerfiles

There are simply 3 steps to follow:

1 - Use an aleph runtime base

`FROM amozpay/aleph-runtime-base:debian-11`

2 - Install packages, do static setup, etc...
```Dockerfile
# Install some additionnal packages as an example
RUN apt-get install curl -y

# remove unwanted packages (be carefull with that, these packages are not required, but that's pretty much it!)
RUN apt-get autoremove nodejs npm -y
```

3 - (Optional) Copy your plugins 
```Dockerfile
COPY ./init0_plugin.sh /root/init0_plugin.sh # this is optionnal 
COPY ./custom_plugins.py /root/custom_plugins.py

# make them executable 
RUN chmod +x /root/custom_plugins.py /root/init0_plugin.sh.py

RUN echo "done!"
```

# Build your runtime

Run `aleph runtime build my_project` to build your runtime.

It will:
- Build the runtime with docker from your Dockerfile
- Export the layers to `my_project/build/my_project.tar`
- Extract the tar archive to `my_project/build/my_project.rootfs`
- Make it into a aleph compatible squashfs archive for performance on the network, in `my_project/build/my_project.squashfs`

