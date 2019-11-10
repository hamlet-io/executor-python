# README

This is a basic instruction on how to launch/test project locally in development environment.

### Dev env setup
You just need to install requirements:
1. ```docker```
1. ```docker-compose```
1. ```make```

### Working in dev env
There are several commands in root **Makefile**:
1. ```make build``` - builds project images
1. ```make clean``` - clears all project related local data including images.
1. ```make run``` - starts project services in detached mode/background
1. ```make run-fg``` - starts project services in attached/foreground mode.

To start you need to run ```make run``` or ```make run-fg```.

After all services launched you need to run ```make ssh-gen3-cli```. This command opens ssh session to gen3-cli dev env service container.

Dev env container **Makefile** has next commands:
1. ```make install``` - builds wheel package and installs it using pip.
1. ```make coverage``` - creates tests coverage report.
1. ```make tests``` - tests project without coverage report.
1. ```make lint``` - lints projects python files.

To live test project in dev env container as cli you need to:
1. ```make install``` - build and install cli
2. ```cot --help``` - get available commands list
