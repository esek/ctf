# Docker from Docker

The CTF server application can be built into a docker image, which runs the task module docker containers in parallel, referred to as the "Docker-from-Docker" approach. 

## Podman
Podman offers some compatibility options to work with pre-existing docker tooling such as the Python SDK. To run the docker features in this project the `podman-docker` packages is required, as well as the creation of the podman docker-like socket: 
`systemctl --user start podman.socket`.