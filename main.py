import geopandas as gpd
import pandas as pd
import csv
import re

# 读取任务点的信息
mission_point = gpd.read_file("data/mission/point.gpkg")
POINT = mission_point.to_csv("POINT.csv")

# 读取任务区域的信息
mission_area = gpd.read_file("data/mission/area.gpkg")
AREA = mission_area.to_csv("AREA.csv")


# 建立点的结构体
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


# 建立区域的结构体
class Mission_area:
    def __init__(self):
        self.geometry = None
        self.mission_id = None
        self.area = None

    def __int__(self):
        pass

    def struct(self, mission_id, area, geometry):
        self.mission_id = mission_id
        self.area = area
        self.geometry = geometry


Point = []


def Point_Processing():
    pdf = pd.read_csv("POINT.csv")
    num_rows = len(pdf)
    # print(num_rows)
    for i in range(num_rows + 1):
        Point.append(Mission_Point())

    d = 0
    with open("POINT.csv", 'r') as csvfile:
        reader = csv.reader(csvfile)
        for i in reader:
            if d == 0:
                d = d + 1
            else:
                # print(i[1])
                Point[d].mission_id = i[1]
                pattern = r'POINT \(([^ ]+) ([^ ]+)\)'  # 正则表达式
                match = re.match(pattern, i[2])
                if match:
                    longitude = float(match.group(1))
                    latitude = float(match.group(2))
                    Point[d].geometry = [longitude, latitude]
                else:
                    print("No match found")
                d = d + 1

    for i in range(10):
        print(Point[i].get_latitude())


def main():
    Point_Processing()


if __name__ == "__main__":
    main()
