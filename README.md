# Distributed Word Count

## Setup venv environment
`sudo apt install python3-venv` 
`which python3`
`cd word_count_task` 
`/usr/bin/python3 -m venv venv`
`source venv/bin/activate`

## Install necessary packages
`pip3 install -r requirements.txt`

## Start worker
`python3 initiate_worker.py`

## Start driver
`python3 initiate_driver.py --N 6 --M 4`

## Start test
`pytest test.py` (after getting the output files)

## Compile Protobuf file 
`python -m grpc_tools.protoc -I proto --python_out=. --grpc_python_out=. proto/driver-service.proto`

## GRPC API
#### Get_Task
Worker asks driver for a task and driver returns the following
- Map Task
- Reduce Task
- Idle Task
- Shutdown Task

#### CountAndInitiateReduce
It counts the number of map tasks completed. If all of them are completed, initiates reduce task.

#### StopReduce
If all reduce tasks are completed, initiate shutdown.
