import yaml
import downloader_scalar as scalar
import downloader_uv as uv
import downloader_vort as vort


def download_all():
    uv.start_download_uv()
    scalar.start_download_whole_cube("salt")
    scalar.start_download_whole_cube("theta")
    print("Start calculating vorticity")
    vort.calc_all_vorticity()
    print("Finished calculating vorticity")


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
                print("Start calculating vorticity")
                vort.calc_all_vorticity()
                print("Finished calculating vorticity")
    else:
        download_all()


if __name__ == '__main__':
    main()
