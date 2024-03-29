# Contributing

Contributions and pull requests are welcome. If you wish to contribute, please
open a new issue first and make it known that you are working on it. I
(Stephen Mitchell) indend on supporting this project for the forseeable future
and will attempt to merge pull requests as often as my schedule permits.

If you find a bug, please create a new issue and tag it as such. Additionally,
please provide the version of the package you found the bug, the desired
behavior, the actual behavior, and any steps needed to reproduce the said
behavior.

# Project Layout

## bin

Contains executable files.

## docs

Documentation for the project.

## realtimepose

Package containing the project's source code.

This project uses a 
[hexagonal architecture](https://en.wikipedia.org/wiki/Hexagonal_architecture_(software)) 
(also called "ports and adapters" architecture)
such that it can more easily support a varied array of inputs, graphical
outputs, and feedback devices. Core business logic is stored in
sub-packages under the `core` package. These include:
- `displaying`: Interfaces and logic for displaying data
<!-- - `feedback_providing`: Interfaces and logic for providing feedback to user -->
<!-- - `logging`: Interfaces and logic for logging  -->
- `recieving`: Interfaces and logic for data input

The interfaces ("Protocols" in python) in these core packages define
"ports", or standards that need to be met in order to interact with the 
program. By implementing these interfaces, concrete classes create 
"adapters" that allow them to "plug in" to the project. 

The rest of the packages under `realtimepose` provide adapters to the ports
defined in `core`. For instance, the `user_interface` package provides
graphical user interface implementations that conform to the `displaying`
core package port (found under `core/displaying/service.py`).

<!-- ## tests

lol -->