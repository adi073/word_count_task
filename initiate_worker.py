#!/usr/bin/python3

import logging
from enum import Enum
import grpc
from google.protobuf.empty_pb2 import Empty

from stub.driver_service_pb2 import TaskType, TaskInfo
from stub.driver_service_pb2_grpc import DriverServiceStub
from mapper_reducer import Mapper, Reducer

class State(Enum):
    Action = 0
    Idle = 1
    Waiting = 2

class Worker:
    def __init__(self):
        self.state = State.Action
        self.mapper = Mapper()
        self.reducer = Reducer()
    
    def get_task(self, SERVER_ADDRESS):
        with grpc.insecure_channel(SERVER_ADDRESS) as channel:
            stub = DriverServiceStub(channel)
            task = stub.GetTask(Empty())
        return task

    def process(self, SERVER_ADDRESS):
        while True:
            try:
                task = self.get_task(SERVER_ADDRESS)
                if task.type == TaskType.Map:
                    self.state = State.Action
                    self.mapper.map(task.id, task.files, task.M)

                elif task.type == TaskType.Reduce:
                    self.state = State.Action
                    self.reducer.reduce(task.id)

                elif task.type == TaskType.Idle:
                    logging.info('Idle')
                    self.state = State.Idle

                else:
                    return
            except grpc._channel._InactiveRpcError:
                # Just one time log driver is unavailable
                if self.state != State.Waiting:
                    logging.info('driver is unavailable')
                    self.state = State.Waiting

if __name__ == "__main__":
    SERVER_ADDRESS = 'localhost:50051'
    worker = Worker()
    worker.process(SERVER_ADDRESS)

