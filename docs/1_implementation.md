# Task Interpretation
#

## Prerequisites 
To run this pipeline, please install the following.

1. [git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
2. [Github account](https://github.com/)
3. [Docker](https://docs.docker.com/engine/install/) and [Docker Compose](https://docs.docker.com/compose/install/)


### Setup infra

Clone your repository and replace content in the following files
1. **[env_sample](https://github.com)**: Rename it to .env and replace the values with your credentials


Run the following commands in your project directory.

```shell
# Run & test
make up # start the docker containers on your computer
make ci # Runs auto formatting, lint checks, & all the test files under ./tests
```

Once airflow is running, create MYSQL connection on airflow web server.
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

**Database schema**
![DE Infra](/images/db.png)

**Blob**

* The content details and descriptions of the news articles are stored in a blob storage.
* The blob storage follows a file system structure where the news items for each day are stored in one json file.

![DE Infra](/images/blob.png)

* Each news Item in the json file is connected to the data in the data base using and ID which is made up of "date and time the article was published, author id and source name" e.g. **2023-04-27T18:30:00Z_beth skwarecki_lifehacker**
## Possible usecases
**Analytics**

* Indetify authors with the most number news during the week.
* Distribution of number of news items over the week.
* Number of authors bellonging who wrote for more than one source during the week.
* Compare number of news during the weekends and weekdays

 **AI Algorithms**

* Clustering of news Items: Algorithm that classifies simillar news Items together to avoid duplication for the end user
* Fake news detection
* Topic modelling: To discover the different themes in the news during the week.

## Possible next steps.
* Update the API start date and end dynamically so the pipeline runs at the end of every week and processes previous week's news.
* Replace the temporary data storage with a database. This will be more efficient when the data volume grows.
* Add data testing step between the temporary file storage and the datalake.
* Indentify countries ***








