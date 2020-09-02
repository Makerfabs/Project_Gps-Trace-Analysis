import gmplot  # 导入模块
import numpy as np
import matplotlib.pyplot as plt
import math

# GPS data
max_time = 0
lat_list = []
lon_list = []
time_list = []
width = 0

# Google map api offset
lat_offset = - 0.00295
lon_offset = 0.0052

# calculate data
distance = []
total_distance = []

speed = []
avg_speed = 0.0


# 从文件中加载GPS数据：经纬度，时间
def read_GPS_data(filename):
    f = open(filename, 'r')
    while True:
        line = f.readline()
        if not line:  # 等价于if line == "":
            break
        if line.find('index') != -1:
            data = eval(line)
            # 纬度
            latitude = data['latitude']
            # 经度
            longitude = data['longitude']
            if latitude != "NULL":
                run_time = data['time']
                time_list.append(run_time)
                lat_list.append(latitude + lat_offset)
                lon_list.append(longitude + lon_offset)

    global width
    width = len(lat_list)
    f.close()
    print("Read over")


def create_html_map():
    # 初始化位置
    gmap = gmplot.GoogleMapPlotter(lat_list[0], lon_list[0], 16)  # 传入经纬度的参数

    # 绘制轨迹
    gmap.plot(lat_list, lon_list)

    # 起始点标记
    gmap.marker(lat_list[0], lon_list[0], color='blue')
    gmap.marker(lat_list[width - 1], lon_list[width - 1], color='red')

    # 生成html
    gmap.draw("./map11.html")  # 绝对路径，绘出地图样貌


def calculate_data():
    print("Empty data")
    if width < 1:
        return
    print("Begin calculate")
    for i in range(1, width):
        temp_distance = math.sqrt(math.pow(
            lon_list[i] - lon_list[i - 1], 2) + math.pow(lat_list[i] - lat_list[i - 1], 2)) * 111319.491
        distance.append(temp_distance)
        if i == 1:
            total_distance.append(temp_distance)
        else:
            total_distance.append(total_distance[i - 2] + temp_distance)

        temp_speed = temp_distance / (time_list[i] - time_list[i-1])
        speed.append(temp_speed)

    global avg_speed
    avg_speed = round(total_distance[-1] / (time_list[-1] - time_list[0]),2)


def main():
    read_GPS_data("./trace4.txt")
    create_html_map()
    calculate_data()

    plt.subplot(2, 1, 1)
    plt.plot(time_list[0:-1], speed)
    plt.title("Average Speed:" + str(avg_speed))
    # plt.xlabel("Time")
    plt.ylabel("Speed(m/s)")
    plt.subplot(2, 1, 2)
    plt.plot(time_list[0:-1], total_distance)
    plt.title("Total Distance:" + str(round(total_distance[- 1],2)))
    plt.xlabel("Time")
    plt.ylabel("Distance(m)")
    plt.draw()
    plt.pause(0)
    pass


if __name__ == "__main__":
    main()
