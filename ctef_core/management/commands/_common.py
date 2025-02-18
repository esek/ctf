DOCKER_NETWORK_ID = "ctef_docker_network"


def module_container_name(module_name):
    """
    Returns the container name given the module name.
    """
    return f"ctef_{module_name}_env"
