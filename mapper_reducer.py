#!/usr/bin/python3

import logging
import os
import grpc
import glob

from google.protobuf.empty_pb2 import Empty
from driver_service_pb2_grpc import DriverServiceStub

INTERMEDIATE_DIR = 'intermediate'
SERVER_ADDRESS = 'localhost:50051'
OUT_DIR = 'out'

class Mapper:
    '''Maps map tasks to intermediate directory'''

    def __init__(self):
        self.file_dict = {}

    def map(self, map_id, files, M):
        logging.info('mapping/saving words to respective intermediate files')
        os.makedirs(INTERMEDIATE_DIR, exist_ok=True)
        for file in files:
            with open(file, 'r') as f:
                words = f.read()
            for word in words.split():
                bucket_id = ord(word[0]) % M
                with open(f'{INTERMEDIATE_DIR}/mr-{map_id}-{bucket_id}', 'a') as intermediate_file:
                    intermediate_file.write(f'{word}\n')
        self.end_mapping()

    def end_mapping(self):
        with grpc.insecure_channel(SERVER_ADDRESS) as channel:
            stub = DriverServiceStub(channel)
            stub.CountAndInitiateReduce(Empty())

class Reducer:
    '''Reduces multiple files from intermediate directory to single files'''
    def __init__(self):
        self.word_dict = {}

    def reduce(self, bucket_id):
        os.makedirs(OUT_DIR, exist_ok=True)
        for _file in glob.glob(f'{INTERMEDIATE_DIR}/mr-*-{bucket_id}'):
            with open(_file) as f:
                for i in f.readlines():
                    i = i.strip()
                    if i not in self.word_dict:
                        self.word_dict[i] = 1
                    else:
                        self.word_dict[i] += 1
        with open(f'{OUT_DIR}/out-{bucket_id}', 'a') as f_out:
            for word, count in self.word_dict.items():
                f_out.write(f"{word} {count}\n")
        self.word_dict = {}
        self.end_reduce()

    def end_reduce(self):
        with grpc.insecure_channel(SERVER_ADDRESS) as channel:
            stub = DriverServiceStub(channel)
            stub.StopReduce(Empty())
