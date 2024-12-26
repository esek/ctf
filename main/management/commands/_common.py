DOCKER_NETWORK_ID = "ctf_docker_network"


def module_container_name(module_name):
    """
    Returns the container name given the module name.
    """
    return f"ctf_{module_name}_env"
