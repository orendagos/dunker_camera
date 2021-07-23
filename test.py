#!/usr/bin/python2.7
import select
import sys
import os
import threading
import time

log=open("./test.log","w")
(reader, writer) = os.pipe()

event = threading.Event()
def reader_handler(num):
    
    while True:
        print("begin to select")
        open_file = os.fdopen(reader, "r")
        input_list = list()
        input_list.append(open_file)
        (readyInput,readyOutput,readyException) = select.select(input_list, [], [])
        for indata in readyInput:
            if indata == open_file:
                # read data
                data = open_file.read()
                print("read data: ", data)
        os.close(open_file)
def reader_handler2(num):
    open_file = os.fdopen(reader, "r")
    time.sleep(2)
    while True:
        print('1111111begin to set', event.isSet())
        # recv = os.read(open_file, 32)
        event.set()
        print('1111111111end set event', event.isSet())
        time.sleep(5)

def writer_handler2(num):
    while True:
        print('22222222222begin to wait', event.isSet())
        event.wait()
        print('222222222222get event', event.isSet())
        event.clear()
        time.sleep(1)

def writer_handler(num):
    while True:
        time.sleep(5)
        open_file = os.fdopen(writer, "w")
        open_file.write("123")
        open_file.close()

t1 = threading.Thread(target=reader_handler2, args=(1200, ))# interval is 2min
t1.start()

t2 = threading.Thread(target=writer_handler2, args=(1200, ))# interval is 2min
t2.start()



