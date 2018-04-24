from ci import command


def test_list_domain():
    command("yunohost domain list")
