##global variables
from datetime import datetime

g_file_dir = "data2"

g_input_rate = "30"
g_output_rate = "30"
g_video_name = "video.mp4"

g_frame_count_weight = 1

#bad quality images
g_rows = []

g_start_time = datetime(2022, 1, 30, 0, 0)
g_end_time = datetime(2022, 2, 2, 12, 20)


###outputs
buffr_blur = []
score_blur = []
pred_blur = [] #blur status of images 


buffr_glare=[]
pred_glare=[] #glare status 
score_glare=[]

name=[]

image_array=[]
