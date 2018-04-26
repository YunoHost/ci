from fabric.api import sudo


def test_list_domain():
    sudo("yunohost domain list")
