import json
import sys

import geopandas as gpd
import pandas as pd
import csv
import re
from shapely.geometry import Polygon

# 读取任务点的信息
mission_point = gpd.read_file("data/mission/point.gpkg")
mission_point.to_csv("POINT.csv")

# 读取任务区域的信息
mission_area = gpd.read_file("data/mission/area.gpkg")
mission_area.to_csv("AREA.csv")

Point = []   # 用于存任务点的信息，下标从1开始记录
Area = []    # 用于存任务区域的信息，下标从1开始记录
Mission = []  # 用于存取任务信息，下标从1开始
Satellite = []  # 用于存取卫星信息，下标从1开始
# ################# 建立点的结构体
class Mission_Point:
    def __init__(self):
        self.geometry = None
        self.mission_id = None
    def __int__(self):
        pass
    def struct(self, mission_id, geometry):
        self.mission_id = mission_id
        self.geometry = geometry
    def get_longitude(self):  # 获取经度
        if self.geometry is not None:
            return self.geometry[0]
        else:
            return None
    def get_latitude(self):  # 获取维度
        if self.geometry is not None:
            return self.geometry[1]
        else:
            return None
# ################# 建立区域的结构体
class Mission_area:
    def __init__(self):
        self.mission_id = None
        self.area = None
        self.geometry = None
    def __int__(self):
        pass
    def struct(self, mission_id, area, geometry):
        self.mission_id = mission_id
        self.area = area
        self.geometry = geometry
# ################# 建立任务的结构体
class MISSION:
    def __init__(self):
        self.score = None
        self.max_time = None
        self.min_time = None
        self.time_interval = None
        self.frequency = None
        self.resolution = None
        self.mission_type = None
        self.mission_id = None
    def __int__(self):
        pass
    def struct(self,mission_id,mission_type,resolution,frequency,time_interval,min_time,max_time,score):
        self.mission_id = mission_id
        self.mission_type = mission_type
        self.resolution = resolution
        self.frequency = frequency
        self.time_interval = time_interval
        self.min_time = min_time
        self.max_time = max_time
        self.score = score
# ################# 建立卫星约束的结构体
class satellite:
    def __init__(self):
        self.satellite_id = None
        self.satellite_type = None
        self.visualfield = None
        self.left_roll = None
        self.right_roll = None
        self.sunlight = None
        self.resolution = None
        self.startup_min = None
        self.orbit_max = None
        self.trantime_0 = None
        self.trantime_10 = None
        self.trantime_20 = None
        self.sunlight_intervals = None
    def __int__(self):
        pass
    def struct(self,satellite_id,satellite_type,visualfield,left_roll,right_roll,sunlight,resolution,startup_min,orbit_max,trantime_0,trantime_10, trantime_20,sunlight_intervals):
        self.satellite_id = satellite_id
        self.satellite_type = satellite_type
        self.visualfield = visualfield
        self.left_roll = left_roll
        self.right_roll = right_roll
        self.sunlight = sunlight
        self.resolution = resolution
        self.startup_min = startup_min
        self.orbit_max = orbit_max
        self.trantime_0 = trantime_0
        self.trantime_10 = trantime_10
        self.trantime_20 = trantime_20
        self.sunlight_intervals = sunlight_intervals


# #################################任务点的处理
def Point_Processing():
    pf = pd.read_csv("POINT.csv")
    num_rows = len(pf)     # 点的个数
    # print(num_rows)
    for i in range(num_rows + 1):
        Point.append(Mission_Point())   # 初始化
    d = 0
    with open("POINT.csv", 'r') as csvfile:
        reader = csv.reader(csvfile)
        for i in reader:
            if d == 0:
                d = d + 1
            else:
                # print(i[1])
                Point[d].mission_id = i[1]
                pattern = r'POINT \(([^ ]+) ([^ ]+)\)'   # 正则表达式
                match = re.match(pattern, i[2])
                if match:
                    longitude = float(match.group(1))
                    latitude = float(match.group(2))
                    Point[d].geometry = [longitude, latitude]   # 存取的信息为[经度， 维度]
                else:
                    print("No match found")
                d = d + 1
    #  Test 获取其中的一个坐标的方式如下
    for i in range(10):
        print(Point[i].get_latitude())

# #################################任务区域的处理
def Area_Processing():
    pf = pd.read_csv("AREA.csv")
    num_rows = len(pf)
    for i in range(num_rows + 1):
        Area.append(Mission_area())
    d = 0
    csv.field_size_limit(10**9)
    with open("AREA.csv", 'r') as csvfile:
        reader = csv.reader(csvfile)
        for i in reader:
            if d == 0:
                d = d + 1
            else:
                # print(i[3])
                polygon_str = i[3]
                # #
                coords_str = polygon_str.replace("POLYGON ((", "").replace("))", "")
                coords = [tuple(map(float, coord.split())) for coord in coords_str.split(",")]
                polygon = Polygon(coords)
                points = list(polygon.exterior.coords)
                # # 以上这段代码是用于将这个多边形的点的坐标给划分出来
                Area[d].geometry = points
                Area[d].mission_id = i[1]
                Area[d].area = i[2]
                d = d + 1
    # Test
    # print(Area[1].mission_id)
    # print(Area[1].area)
    print(Area[2].geometry)
# #################################任务的处理
def Mission_Processing():
    pf = pd.read_csv("data/mission/mission.csv")
    num_rows = len(pf)
    for i in range(num_rows + 1):
        Mission.append(MISSION())
    d = 0
    with open("data/mission/mission.csv", 'r') as csvfile:
        reader = csv.reader(csvfile)
        for i in reader:
            if d == 0:
                d = d + 1
            else:
                # mission_id,mission_type,resolution,frequency,time_interval,min_time,max_time,score
                Mission[d].mission_id = i[0]
                Mission[d].mission_type = i[1]
                Mission[d].resolution = i[2]
                Mission[d].frequency = i[3]
                Mission[d].time_interval = i[4]
                Mission[d].min_time = i[5]
                Mission[d].max_time = i[6]
                Mission[d].score = i[7]
                d = d + 1
    # Test
    # print(Mission[1].score)

def Satellite_Processing():
    pf = pd.read_csv("data/satellite/satellite.csv")
    num_rows = len(pf)
    for i in range(num_rows + 1):
        Satellite.append(satellite())
    print(num_rows)
    csv.field_size_limit(10 ** 9)
    d = 0
    with open("data/satellite/satellite.csv", 'r') as csvfile:
        reader = csv.reader(csvfile)
        for i in reader:
            if d == 0:
                d = d + 1
            else:
                # satellite_id,satellite_type,left_roll,right_roll,sunlight,resolution,startup_min,orbit_max,trantime_0,trantime_10, trantime_20,sunlight_intervals
                Satellite[d].satellite_id = i[0]
                Satellite[d].satellite_type = i[1]
                Satellite[d].visualfield = i[2]
                Satellite[d].left_roll = i[3]
                Satellite[d].right_roll = i[4]
                Satellite[d].sunlight = i[5]
                Satellite[d].resolution = i[6]
                Satellite[d].startup_min = i[7]
                Satellite[d].orbit_max = i[8]
                Satellite[d].trantime_0 = i[9]
                Satellite[d].trantime_10 = i[10]
                Satellite[d].trantime_20 = i[11]
                intervals = json.loads(i[12])
                coordinates = [(interval[0], interval[1]) for interval in intervals]
                Satellite[d].sunlight_intervals = coordinates
                d = d + 1
    # Test   直接获取某个区间的值
    # for i in range(1,10):
    #     print(Satellite[i].sunlight_intervals[1])
def main():
    Point_Processing()
    Area_Processing()
    Mission_Processing()
    Satellite_Processing()

if __name__ == "__main__":
    main()
