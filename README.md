# [repository name]
[repository description]

## Requirements

## Getting started
There are shell scripts in [scripts/](scripts) directory:
- [install.sh](scripts%2Finstall.sh): This should contain all the commands to **install** the project.
- [run.sh](scripts%2Frun.sh): This should contain all the commands to **run** the project.

After cloning the repository, run the following commands:
```sh
$ cd [repository name]
$ bash scripts/install.sh
```
To install all needed dependencies, then, to run the project (for eg. start a web server, start a training, etc.)
```sh
$ bash scripts/run.sh
```

## Contribution 
There are two main branches:
- develop: This branch is used to develop new features. You can merge your feature branch into develop once done.
- main: This branch is protected, you can't push directly to it. You have to create a pull request from develop to main and ask for a review.