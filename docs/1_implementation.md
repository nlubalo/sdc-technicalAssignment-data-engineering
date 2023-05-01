# Task Interpretation
#

## Prerequisites 
To run this pipeline, please install the following.

1. [git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
2. [Github account](https://github.com/)
3. [Docker](https://docs.docker.com/engine/install/) and [Docker Compose](https://docs.docker.com/compose/install/)


### Setup infra

Clone your repository and replace content in the following files

Run the following commands in your project directory.

```shell
# Run & test
make up # start the docker containers on your computer
make ci # Runs auto formatting, lint checks, & all the test files under ./tests
```

## Tear down infrastructure

When done run the command below to tear down the infrastructure

```shell
make down # Stop docker containers on your computer
```

**Data infrastructure**
![DE Infra](/images/infra.png)



### Project Structure:

* `./dags` - `DAG_FOLDER` for DAG files
* `./logs` - contains logs from task execution and scheduler.
* `./plugins` - for custom plugins
* `./data` - stores temporary transformed data and blob storage data lake

## Final data structure

The final data structure 

## Possible next steps.
* Update the API start date and end dynamically so the pipeline runs at the end of every week and processes previous week's news.
* Replace the temporary data storage with a database. This will be more efficient when the data volume grows.
* Add data testing step between the temporary file storage and the datalake.
* Indentify countries ***








