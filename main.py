import re
from datetime import datetime
import shutil
import tkinter as tk
from tkcalendar import Calendar
from tktimepicker import SpinTimePickerOld
from globalVar import *
from readdir import *
from tktimepicker import constants
from generate import *
from tkVideoPlayer import TkinterVideo

# ->directory for images
folder_path = "./userdata"

def on_closing():
	# Clean up any resources or perform necessary actions before closing the window
	window.destroy()  # Close the Tkinter window

class ImageGUI:
   
	def __init__(self, master):
		self.master = master
		self.master.title("Image GUI")
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------   
	# Section to handle all the frames in the entire Tkinter window
		
		# Create a frame for displaying the video and center it
		self.video_frame = tk.Frame(self.master, highlightbackground="black", highlightthickness=5)

		# Create frame 1 for displaying image loading button
		self.button_frame1 = tk.Frame(self.master, highlightbackground="black", highlightthickness=5)

		# Create frame 2 for date selection and time interval options
		self.button_frame2 = tk.Frame(self.master, highlightbackground="black", highlightthickness=5)

		# Create frame 2 for displaying process video button
		self.button_frame3 = tk.Frame(self.master, highlightbackground="black", highlightthickness=5)

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------       
	# Section to handle load image button 
		
		# Create a "Load Image" button
		self.load_button = tk.Button(self.button_frame1, text="Load Image", command=self.load_images)
		self.load_button.pack(side=tk.TOP, padx=10, pady=10)
		
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- 
	# Section for input parameters handling

		# ->Create a calendar widget for start date selection
		self.calendar_start = Calendar(self.button_frame2, selectmode = 'day', year = 2022, month = 1, day = 1)

		# ->Create a calendar widget for end date selection
		self.calendar_end = Calendar(self.button_frame2, selectmode = 'day', year = 2022, month = 2, day = 22)

		# ->Create start time label
		self.time_picker_start_label = tk.Label(self.button_frame2, text="Start Time")

		# ->Create a time picker widget for starting time
		self.time_picker_start = SpinTimePickerOld(self.button_frame2)
		self.time_picker_start.addAll(constants.HOURS24)

		# ->Create end time label
		self.time_picker_end_label = tk.Label(self.button_frame2, text="End Time")

		# ->Create a time picker widget for ending time
		self.time_picker_end = SpinTimePickerOld(self.button_frame2)
		self.time_picker_end.addAll(constants.HOURS24)

		# ->Pack all the buttons and widgets
		self.calendar_start.pack(side=tk.LEFT, padx=10, pady=10)
		self.calendar_end.pack(side=tk.LEFT, padx=10, pady=10)  
		self.time_picker_start_label.pack(side=tk.TOP, padx=10, pady=10)
		self.time_picker_start.pack(side=tk.TOP, padx=10, pady=10)
		self.time_picker_end_label.pack(side=tk.TOP, padx=10, pady=10)
		self.time_picker_end.pack(side=tk.TOP, padx=10, pady=10)

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------       
	# Section to handle threshold slider and process video button 

		# ->Create a slider to adjust the blur threshold
		self.blur_threshold = tk.IntVar()
		self.blur_threshold.set(90)
		self.blur_threshold_scale = tk.Scale(self.button_frame3, from_=1, to=100, digits = 3, orient=tk.HORIZONTAL, label="Threshold", variable=self.blur_threshold)
		self.blur_threshold_scale.pack(side=tk.TOP, padx=10, pady=10)

		# ->Create a slider to adjust the blur threshold
		self.glare_threshold = tk.IntVar()
		self.glare_threshold.set(60)
		self.glare_threshold_scale = tk.Scale(self.button_frame3, from_=1, to=100, digits = 3, orient=tk.HORIZONTAL, label="Threshold", variable=self.glare_threshold)
		self.glare_threshold_scale.pack(side=tk.TOP, padx=10, pady=10)
		
		# Create a "Process Video" button
		self.video_button = tk.Button(self.button_frame3, text="Process Video", command=self.process_images)
		self.video_button.pack(side=tk.TOP, padx=10, pady=10)
		
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------      
	# Section to pack all the tkinter frames
		
		# Pack all the frames
		self.video_frame.pack(side = tk.TOP, expand = True, fill = tk.BOTH)
		self.button_frame1.pack(side = tk.LEFT, expand = True, fill = tk.BOTH)
		self.button_frame2.pack(side = tk.LEFT, expand = True, fill = tk.BOTH)
		self.button_frame3.pack(side = tk.LEFT, expand = True, fill = tk.BOTH)

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Function to load images from the mentioned date and time intervals

	def load_images(self):

		# ->Configuring start date and time variables
		start_date = self.calendar_start.get_date()
		start_time = self.time_picker_start.time()
		g_start_time = datetime(int(start_date.split("/")[1]), int(start_date.split("/")[0]), int(start_date.split("/")[2]), int(start_time[0]), int(start_time[1]))

		# ->Configuring end date and time variables
		end_date = self.calendar_end.get_date()
		end_time = self.time_picker_end.time()
		g_end_time = datetime(int(end_date.split("/")[1]), int(end_date.split("/")[0]), int(end_date.split("/")[2]), int(end_time[0]), int(end_time[1]))

		print(g_start_time, g_end_time)

		file_list = extract_files_from_folder(folder_path)
		pattern = r'[/\\](\d+)[/\\](\d+)[/\\](\d+)[/\\](\d+)[-\\](\d+)'

		outputDir = g_file_dir
	
		for file in file_list:
			match = re.search(pattern, file.filepath)
			v1 = match.group(1)
			groups = match.groups()
			if match:
				year, month, day, hour, minutes = map(int, match.groups())
				file.timestamp = datetime(year, month, day, hour, minutes)

		count = 1
		writer = open(f"{outputDir}/time.txt","w")
		for file in file_list:
			source_file = file.filepath

			date_time = file.timestamp.strftime("%Y-%m-%d-%H-%M")
			destination_file = f'{outputDir}/destination{count}.jpg'  # target file path
			writer.write(f"{date_time}_1\n")

			#copy to new directory
			shutil.copy(source_file, destination_file)
			count +=1 

		writer.close()
		print("done")

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Function to Process video from the images and display it 
	def process_images(self):
		generate(self.blur_threshold, self.glare_threshold)

		def loop(e):
			videoplayer.play()

		videoplayer = TkinterVideo(master=self.video_frame, scaled=True)
		videoplayer.load(r"video.mp4")
		videoplayer.pack(side=tk.TOP, padx=10, pady=10, expand=True, fill="both")
		videoplayer.play()
	
		videoplayer.bind("<<Ended>>", loop)
	


# Instantiate a window from the class
if __name__ == "__main__":
	window = tk.Tk()
	window.geometry("900x900")
	gui = ImageGUI(window)
	window.mainloop()