# PJM Electricity Load Forecaster API
The purpose of this project is to demonstrate training and serving a model using Docker and Amazon Sagemaker. This is useful for deploying the model in a production environment, where it can be continuously updated and accessed. The model itself is a very simple ARIMA model that forecasts electricity load in one of two areas within the PJM Interconnection territory. 

## Source data
The source data were two csv files with instantaneous load values (at fifteen-minute intervals) for December 2020 from the PEPCO (PEP) and PECO (PE) areas within PJM. The data can be freely downloaded using PJM's [Data Miner 2 tool](http://dataminer2.pjm.com/feed/inst_load). 

The raw data looks like:
```
datetime_beginning_utc,datetime_beginning_ept,area,instantaneous_load
1/1/2021 4:55:00 AM,12/31/2020 11:55:00 PM,PEP,3016.800000
1/1/2021 4:50:00 AM,12/31/2020 11:50:00 PM,PEP,3016.800000
1/1/2021 4:45:00 AM,12/31/2020 11:45:00 PM,PEP,3020.900000
1/1/2021 4:40:00 AM,12/31/2020 11:40:00 PM,PEP,3018.200000
1/1/2021 4:35:00 AM,12/31/2020 11:35:00 PM,PEP,3044.200000
```

## Train & Deploy Model with Docker
Follow these steps to train and deploy the model locally using Docker and then call the endpoint to get predictions. The `run_local` directory contains helper scripts to use the model locally. 

1. Get Docker: https://www.docker.com/products/docker-desktop
1. Run `sh build_docker_image.sh` to create an image for training and serving the model
1. `cd run_local`
1. Train the model with `sh train.sh`, updating the paths to the training data and a directory to hold the trained model binary. Docker will start a container and mount corresponding paths inside the container to these directories to copy the training data as well as save the trained model binary to your machine so it persists after the container is terminated. 
1. Deploy the trained model with `sh deploy.sh`, updating the path to the directory with the trained model binary from the prior step. The nginx server should start and load the model binary. You will see the following in your console:
    ```
    9hy19fvnr4-algo-1-5bom2 | Starting the inference server with 4 workers.
    9hy19fvnr4-algo-1-5bom2 | [2021-01-28 20:41:33 +0000] [20] [INFO] Starting gunicorn 20.0.4
    9hy19fvnr4-algo-1-5bom2 | [2021-01-28 20:41:33 +0000] [20] [INFO] Listening at: unix:/tmp/gunicorn.sock (20)
    9hy19fvnr4-algo-1-5bom2 | [2021-01-28 20:41:33 +0000] [20] [INFO] Using worker: gevent
    9hy19fvnr4-algo-1-5bom2 | [2021-01-28 20:41:33 +0000] [23] [INFO] Booting worker with pid: 23
    9hy19fvnr4-algo-1-5bom2 | [2021-01-28 20:41:33 +0000] [24] [INFO] Booting worker with pid: 24
    9hy19fvnr4-algo-1-5bom2 | [2021-01-28 20:41:33 +0000] [25] [INFO] Booting worker with pid: 25
    9hy19fvnr4-algo-1-5bom2 | [2021-01-28 20:41:33 +0000] [26] [INFO] Booting worker with pid: 26
    !9hy19fvnr4-algo-1-5bom2 | 172.20.0.1 - - [28/Jan/2021:20:41:35 +0000] "GET /ping HTTP/1.1" 200 1 "-" "python-urllib3/1.26.2"
    ```
1. Get a prediction by starting a new terminal window, navigating to the `run_local` directory and running `sh get_prediction.sh`. You should get a response back that looks like:
    ```
    2797.04 MW
    ```
   You can of course change the input parameters in the shell script or directly run `python -m predict date time {PE,PEP} http://localhost:8080/invocations`. Each time you call the endpoint, you will see a message printed to the console that is running the nginx server.
