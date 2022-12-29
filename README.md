# Aleph.im Lambda Runtime SDK

![Logo](https://www.aleph.im/assets/img/logo-wide.1832dbae.svg)

Aleph.im's peer to peer network allows execution of programs as lamda functions on it's nodes.
Upon uploading of a program, a user is free to choose a runtime that will execute his code.
The base official Aleph runtimes support exectuting Python ASGI code, Nodejs code, and binary code.

Some users may want to use different tools to meet their purposes, in which case they will want to 
use a custom runtime. This allows, for example, the use of an other programming language, installation of
required libraires, and so forth.

This SDK allows users to easily create and customize a runtime to suit their needs.

# Get Started

Install the [aleph cli](https://github.com/aleph-im/aleph-client) and run the following command to start building your own runtime

`aleph runtime init <OUTPUT_DIRECTORY>` **Not implemented yet**

Build your runtime:
Go to the project root and run

`aleph runtime build <OUTPUT>` **Not implemented yet**

Upload your runtime

`aleph runtime upload <RUNTIME>` **Not implemented yet**

For additional information on the available cli commands and options, see the [aleph cli reference](https://github.com/aleph-im/aleph-client)

# What is a runtime?

The word runtime may designated different things, but in our case, a runtime is defined
by the root folder and file architecture that will be used during the lambda function call.

To make it simpler, here's an example:

```bash
ls /

output:
afs  bin  boot  dev  etc  home  lib  lib64  lost+found  media  mnt  opt  proc  root  run  sbin  srv  sys  tmp  usr  var
```

You got it, this root folder you just ls'd is what you could call an Aleph.im runtime.

Some adaptation is required to make it useable, but that's the spirit!

# Create your own runtime

Learn about each component, or follow the [overall tutorial](./tutorials/overall.md) 

## Runtime components

In order to build your own runtime, you need to understand the followings components and their role.

### Init sequence

The init sequence is the first program that will be exectuted when the runtime is loaded.
It is in charge of mounting devices and volumes, of receiving information from the Aleph network and of calling the user program listening on port 8080.
It basically does all the setup steps before the program receives data.

[Main init steps](./tutorials/1-init.md)


### Plugins

Most of the time, you might just want to install a package in the runtime.
But if you need to customize the init sequence simply, you can use plugins.

During the init sequence, plugins can be executed at different times to do additional setup.
They consist of python functions that you can create, and that can be called before or after each setup step.


[Create your plugins](./tutorials/2-plugins.md)


### Build system

The first step to build a runtime is to create a linux root folder containing all the files necessary for the execution of a program.
You could create one yourself, or with debootstrap.

We provide a base root folder as a Docker image, so that you can build on it with simple command and Dockerfiles.

Once the root folder is created, it needs to be stored as a squashfs archive.

[Build your runtime](./tutorials/3-build.md)

