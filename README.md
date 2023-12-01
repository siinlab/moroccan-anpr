> Make sure to change the port `9000` name in the `scripts/port.txt` file.
> Make sure to change the value of `IMAGE_NAME` .

# [repository name]
[repository description]

## Requirements

## Getting started
This demo is self-contained and can be built and run on any machine with Docker installed.   
Simply run: `bash scripts/build-image.sh` to build the Docker image.  
Then run: `bash scripts/run.sh` to start the container.

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