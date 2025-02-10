import yaml
import utils
import json
import downloader_scalar as scalar
import downloader_uv as uv
import downloader_vort as vort


def download_all():
    uv.start_download_uv()
    scalar.start_download_whole_cube("salt")
    scalar.start_download_whole_cube("theta")
    print("Start calculating vorticity")
    vort.calc_all_vorticity()
    utils.write_min_max_vort()
    print("Finished calculating vorticity")


def main():
    with open('/config.yml', 'r') as file:
        config = yaml.safe_load(file)

    data = utils.load_json()
    data["size_km"] = utils.get_km_of_config(config)
    print("Write to json:")
    print(data)
    with open('/metadata.json', 'w') as file:
        json.dump(data, file, indent=4)
    print("Done writing to json")

    if bool(config.get("variables")):
        # Download LIC textures
        uv.start_download_uv()

        for variable in config["variables"]:
            if variable in ["salt", "theta"]:
                scalar.start_download_whole_cube(variable)
            elif variable == "vorticity":
                print("Start calculating vorticity")
                vort.calc_all_vorticity()
                utils.write_min_max_vort()
                print("Finished calculating vorticity")
    else:
        download_all()


if __name__ == '__main__':
    main()
