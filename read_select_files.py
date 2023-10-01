import os 
import re
import ctypes
import subprocess
from datetime import datetime
from globalVar import *

class File:
  def __init__(self):
      self.filepath= ""
      self.timestamp = None

def binary_search(datetimelist, target):
    left, right = 0, len(datetimelist) - 1
    isRight = False
    while left <= right:
        mid = left + (right - left) // 2

        # 如果目标值等于中间值，返回中间索引
        if datetimelist[mid]== target:
            return mid

        # 如果目标值小于中间值，继续在左半部分搜索
        elif datetimelist[mid] > target:
            isRight = True
            right = mid - 1

        # 如果目标值大于中间值，继续在右半部分搜索
        else:
            isRight = False
            left = mid + 1

    # 如果目标值不在数组中，返回-1表示未找到
    if isRight:
        return right+1
    return left

#use it to find the files between start_time and end_time
def select_files(file_dir, start_time, end_time ):
    file_list = []
    pattern = r'(\d{4})-(\d{2})-(\d{2})-(\d{2})-(\d{2})'

    #find start index and end index
    datetimelist = []
    uselist = []
    with open(f"{file_dir}/time.txt","r") as tf:
        for row in tf:
            row = row.strip()
            use = int(row[-1])
            match = re.search(pattern, row)
            if match:
                year, month, day, hour, minutes = map(int, match.groups())
                timestamp = datetime(year, month, day, hour, minutes)
                datetimelist.append(timestamp)
                uselist.append(use)
            else:
                assert(False)

    start_index = binary_search(datetimelist, start_time)
    end_index = binary_search(datetimelist, end_time)

    image_list = []
    for i in range(start_index, end_index):
        if uselist[i] == 1:
            image_list.append(f"{g_file_dir}/destination{i+1}.jpg")
        
    return image_list

def select_and_make_video(file_dir, start_time, end_time):
    image_list = select_files(file_dir, start_time, end_time)
    frame_count = len(image_list)

    #create text file!
    count = 1
    read_list_file = f"read_list.txt"
    with open(read_list_file,"w") as writer:
        for image in image_list:
            writer.write(f"file '{image}'\n")
    ffmpeg_command = f"ffmpeg -r {g_input_rate} -f concat -safe 0 -i {read_list_file} -c:v libx264 -r {g_output_rate} -pix_fmt yuv420p -frames:v {frame_count * g_frame_count_weight} {g_video_name}"
    
    # for image in image_list:
    #     os.symlink(image, f"{g_file_dir}/link{count}.jpg.lnk")
    #     count += 1

    #ffmpeg_command = f"ffmpeg -r {g_input_rate} -start_number 1 -i {g_file_dir}/link%d.jpg.lnk -c:v libx264 -r {g_output_rate} -pix_fmt yuv420p -frames:v {frame_count * g_frame_count_weight} {g_video_name}"
    #ffmpeg_command = f"ffmpge -r {g_input_rate} -i " +" -i " .join(image_list) +f" -c:v libx264 -r {g_output_rate} -pix_fmt yuv420p -frames:v {frame_count * g_frame_count_weight} {g_video_name}"
  
    print(ffmpeg_command)
    subprocess.run(ffmpeg_command)


if __name__ == "__main__":
    select_and_make_video(g_file_dir, g_start_time, g_end_time)
    print("done")
    
    