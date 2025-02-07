# DeepVis Pipeline

Code of the Docker image of the DeepVis data pipeline.

## Requirements

All Scripts are run in a Docker container. Therefore a Docker installation is needed. More information are available [here](https://docs.docker.com/engine/install/)


## TMP COMMANDS
docker build -t deepvis-pipeline .
docker run -it -v %cd%\config.yml:/config.yml -v %cd%\data:/data --rm --name dvp deepvis-pipeline bash
