import yaml
import downloader_scalar as scalar
import downloader_uv as uv


def download_all():
    #TODO: Implement download_all
    return 0


def main():
    with open('/config.yml', 'r') as file:
        config = yaml.safe_load(file)

    if bool(config.get("variables")):
        # Download LIC textures
        uv.start_download_uv()

        for variable in config["variables"]:
            # TODO: Welche gibt es schon? Und abhängig davon wird Startdatum gesetzt

            if variable in ["salt", "theta"]:
                scalar.start_download_whole_cube(variable)
            elif variable == "voriticity":
                #TODO: Voritcity
                pass
    else:
        download_all()


if __name__ == '__main__':
    main()
