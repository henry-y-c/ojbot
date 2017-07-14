"""Sweep-distance visualization"""
import serial, queue, threading
import numpy as np
from modules.point_cloud_graph import PointCloudGraph
from modules.sweep_dist_parser import to_numbers
import random, sched, time
from PyQt5 import QtCore

class DataBuffer:
    def __init__(self):
        self.cond = threading.Condition()
        self.data = []


    def add(self, newData):
        with self.cond:
            self.data.append(newData)
            self.cond.notify() # Wake 1 thread waiting on cond (if any)

    def getAll(self, blocking=False):
        with self.cond:
            # If blocking is true, always return at least 1 item
            while blocking and len(self.data) == 0:
                self.cond.wait()
            allData, self.data = self.data, []
        return allData

# Initialize data buffer
buffer = DataBuffer()

# Serial LiDAR Lite
def lidar_thread(buffer):
    ser = serial.Serial('/dev/cu.usbmodem1411', 115200)
    while True:
        line = ser.readline().decode('utf-8')
        status, result = to_numbers(line)
        if status:
            data = np.array(spherical_to_cartesian(result)).reshape(1,3)
            buffer.add(data)

try:
   threading.Thread(target=lidar_thread, args=(buffer,)).start()
except:
   print("Error: unable to start thread")

# # Fake data for testing
# def fake_lidar():
#     dataEntry = np.array([random.uniform(0, 180), random.uniform(1, 180), random.uniform(20, 200)]).reshape(1,3)
#     buffer.add(dataEntry)

# def periodic(scheduler, interval, action, actionargs=()):
#     scheduler.enter(interval, 1, periodic,
#                     (scheduler, interval, action, actionargs))
#     action(*actionargs)
    
# def lidar_thread():
#     scheduler = sched.scheduler(time.time, time.sleep)
#     periodic(scheduler, 0.01, fake_lidar)
#     scheduler.run()

# try:
#    threading.Thread(target=lidar_thread).start()
# except:
#    print("Error: unable to start thread")

# Spherical to Cartesian
def spherical_to_cartesian(spherical):
    yaw = np.radians(spherical[0])
    pitch = np.radians(spherical[1])
    dist = spherical[2] + 4.6 # distance from sensor to pivot
    x = dist * np.cos(pitch) * np.sin(yaw)
    y = dist * np.cos(pitch) * np.cos(yaw)
    z = dist * np.sin(pitch)
    return [x, y, z]

# Plot the point cloud graph
graph = PointCloudGraph(buffer)

def plotLoop():
    dataArray = buffer.getAll()
    graph.addDataArray(dataArray)

t = QtCore.QTimer()
t.timeout.connect(plotLoop)
t.start(2000)

graph.start()
