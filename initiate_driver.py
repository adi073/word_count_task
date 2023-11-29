#!/usr/bin/python3
'''script for initializing driver'''

import glob
import logging
import argparse
import grpc
import collections
from threading import Lock, Event
from concurrent import futures
import time

from google.protobuf.empty_pb2 import Empty
from driver_service_pb2_grpc import DriverServiceServicer
from driver_service_pb2_grpc import add_DriverServiceServicer_to_server
from driver_service_pb2 import TaskInfo, TaskType

class DriverService(DriverServiceServicer):
    def __init__(self, N, M):
        self.N = N
        self.M = M
        self.lock = Lock()
        self.files = self.assign_map_id_to_files(N)
        self.state = TaskType.Map
        self.task_id = 0
        self.count = 0
        self.start_time = 0
        self.stop_event = Event()

    @staticmethod
    def assign_map_id_to_files(N):
        '''calculate map id and assign to files'''
        file_dict = collections.defaultdict(list)
        files = glob.glob('inputs/*')
        for i, file in enumerate(files):
            map_id = i % N
            file_dict[map_id].append(file)
        return file_dict

    def GetTask(self, request: Empty, context: grpc.ServicerContext):
        '''get next task'''
        with self.lock:
            if self.state == TaskType.Map:
                return self.map_task()
            if self.state == TaskType.Reduce:
                return self.reduce_task()
            return TaskInfo(type=self.state)

    def CountAndInitiateReduce(self, request: Empty, context: grpc.ServicerContext):
        '''Count the map tasks and start reduce task if count equals N'''
        with self.lock:
            self.count += 1

            if self.count == self.N:
                self.state = TaskType.Reduce
                self.task_id = 0
                self.count = 0
            return Empty()

    def StopReduce(self, request: Empty, context: grpc.ServicerContext):
        '''count all reduce tasks finished'''
        with self.lock:
            self.count += 1

            if self.count == self.M:
                self.state = TaskType.ShutDown
                self.stop_event.set()
            return Empty()

    def map_task(self):
        '''Determines the next Map task and updates the state'''
        map_id = self.task_id
        self.task_id += 1
        if map_id == self.N - 1:
            self.state = TaskType.Idle
        if map_id == 0:
            self.start_time = time.time()
        logging.info('starting map %d', map_id)
        return TaskInfo(type=TaskType.Map, id=map_id, files=self.files[map_id], M=self.M)

    def reduce_task(self):
        '''Determines the next Reduce task and updates the state'''
        bucket_id = self.task_id
        self.task_id += 1
        if bucket_id == self.M - 1:
            self.state = TaskType.Idle
        logging.info('starting reduce %d', bucket_id)
        return TaskInfo(type=TaskType.Reduce, id=bucket_id)


def start_server(service, port):
    '''function to start server'''
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_DriverServiceServicer_to_server(service, server)
    server.add_insecure_port(f"[::]:{port}")
    server.start()
    print("-----------SERVER STARTED----------")
    service.stop_event.wait()
    # Wait to all the workers shut down
    time.sleep(0.5)
    server.stop(0)
    print('-----------SERVER STOPPED----------')


if __name__ == "__main__":
    logging.basicConfig()
    parser = argparse.ArgumentParser()
    parser.add_argument('--N', type=int, required=True, help='Number of map tasks')
    parser.add_argument('--M', type=int, required=True, help='number of reduce tasks')
    args = parser.parse_args()

    service = DriverService(args.N, args.M)
    start_server(service, '50051')
