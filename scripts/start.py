import yaml
import downloader_scalar as scalar


def download_all():
    #TODO: Implement download_all
    return 0


def main():
    with open('/config.yml', 'r') as file:
        config = yaml.safe_load(file)

    if bool(config.get("variables")):
        for variable in config["variables"]:
            if variable in ["salt", "theta"]:
                scalar.start_download_whole_cube(variable)
            elif variable == "uvw":
                #TODO: implemment uvw
                pass
            elif variable == "voriticity":
                #TODO: Voritcity
                pass

    else:
        download_all()


if __name__ == '__main__':
    main()
