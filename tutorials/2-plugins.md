# Create your plugins

If you haven't done it, you should probably go read [this init tutorial](./1-init.md`)

## Register your plugins

Let's create and register a plugin together.

A plugin is a simple Python function, which takes a object as parameter.

If you've created a project with `aleph runtime init my_project`, then the file you will work on should be `my_project/plugins/custom_plugins.py`

First, import `Plugins` from `runtime_types`

```python
from runtime_types import Plugins

```

Plugins can be called before and after each of these steps of the runtime lifecycle (except for shutdown, it can only be called before):
- hostname setup
- environment variables setup
- volume setup
- network setup
- the whole setup process
- shutdown # todo

These are the available plugins parameters, in lifecycle order:

before_system (the setup process) -> before_hostname -> after_hostname -> before_variables -> after_variables -> before_volumes -> after_volumes -> before_network -> after_network -> after_system -> before_shutdown

let's create a plugin that modifies some environment variables


```python
def react_variables_plugin(vars: Dict[str, str]):
    keys_to_change = []
    for key, value in vars.items():
        if key.startswith("REACT_"):
            keys_to_change.append((key, value))
    for key, value in keys_to_change:
        vars.pop(key)
        key = key.replace("REACT_", "")
        vars[key] = value
```

Now, environment variables like `REACT_MY_VAR` will be renamed like `MY_VAR`.
They haven't been exported to the actual environment yet.


These are the available plugins parameters, in lifecycle order:

before_system (the setup process) -> before_hostname -> after_hostname -> before_variables -> after_variables -> before_volumes -> after_volumes -> before_network -> after_network -> after_system -> before_shutdown

We want to run that before the environment variables are set up.

Let's register it by creating the global variable `custom_plugins`

```python
custom_plugins = Plugins(
    before_variables=react_variables_plugin
)
```

Let's also print the environment once it's set up

```python
def colored_print(txt: str):
    print(f"\033[2;31m{txt}\033[0;0m")

def print_environment(vars: Dict[str, str]):
    print("printing the environment variable Dict:")
    print(vars)
    print("\nNow printing os.environ")
    for key, value in dict(os.environ).items():
        if key in vars.keys():
            colored_print(f"{key}={value}")
        else:
            print(f"{key}={value}")
```

Great! Let's add it to the registered plugins.

```python
custom_plugins = Plugins(
    before_variables=react_variables_plugin,
    after_variables=print_environment
)
```

Now we want to test our code.
To test it quickly, let's run `python3 my_project/plugins/tests.py`
Most setup commands, in this test, are just replaced with dummy commands, so you can run it locally.
The test suite will be improved in the future.

# TODO: use Python Init Workshop to create better tests with firecracker