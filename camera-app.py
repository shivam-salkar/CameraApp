'''
python-version: 3.10.0
github: https://github.com/shivam-salkar/CameraApp
'''

from customtkinter import * # type: ignore
from PIL import Image
import PIL
import cv2 as cv
import datetime
import mediapipe as mp
import os
import time
os.makedirs("Photos", exist_ok=True)
os.makedirs("Videos", exist_ok=True)

#--------------------FUNCTIONS----------------------

# GLOBAL VARIABLES
to_save_image = False
is_grayscale = False
settings_window = None
is_face_detection = True
is_flipped = True
to_save_video = False
is_recording = False
start_recording = False
recording_start_time = 0
video_out = None

# FUNCTIONS
def photo_button_click():
    global to_save_image
    
    to_save_image = True

    save_label = CTkLabel(app, text="Photo Saved!", font=("Segoe UI", 18))
    save_label.place(relx=0.5, rely=0.05, anchor="n")
    app.after(1000, save_label.destroy)

def bw_button_click():
    global is_grayscale
    is_grayscale = not is_grayscale

def settings_button_click():
    global settings_window
    global face_detection_textvar
    global is_flipped_textvar

    if settings_window == None or not settings_window.winfo_exists():
        settings_window = CTkToplevel()
        settings_window.geometry('500x300')
        settings_window.title('Settings')
        settings_window.attributes("-topmost", True)
        settings_window.resizable(False, False)
        
        
        face_detection_checkbox = CTkCheckBox(settings_window, text="Face Detection", command=is_face_detection_checkbox, onvalue="on", offvalue="off", variable=face_detection_textvar, font=("Segoe UI", 18))
        face_detection_checkbox.pack()

        
        is_flipped_checkbox = CTkCheckBox(settings_window, text="Mirror Camera", command=is_flipped_clicked_checkbox, onvalue="on", offvalue="off", variable=is_flipped_textvar, font=("Segoe UI", 18))
        is_flipped_checkbox.pack(padx=10, pady=10)

        about_label = CTkLabel(settings_window, text='~ Made by Shivam', font=("Segoe UI", 18))
        about_label.pack(padx=10, pady=10, anchor='s')

        settings_window.focus()
    else:
        settings_window.focus()
    

def is_face_detection_checkbox():
    global is_face_detection
    if is_face_detection:
        is_face_detection = False
    else:
        is_face_detection = True

def is_flipped_clicked_checkbox():
    global is_flipped
    if is_flipped:
        is_flipped = False
    else:
        is_flipped = True

def disable_buttons():
    photo_button.configure(state='disabled', image=camera_icon_d, require_redraw=False)
    settings_button.configure(state='disabled', image=settings_icon_d, require_redraw=False)
    bw_button.configure(state='disabled', image=bw_icon_d, require_redraw=False)
    

def enable_buttons():
    photo_button.configure(state='normal', require_redraw=False, image=camera_icon)
    settings_button.configure(state='normal', require_redraw=False, image=settings_icon)
    bw_button.configure(state='normal', require_redraw=False, image=bw_icon)

def video_button_clicked():
    global is_recording, video_out, recording_start_time

    is_recording = not is_recording

    if is_recording:
        
        x = datetime.datetime.now()
        filename = f"Videos/{x.strftime('%Y')}-{x.strftime('%H')}-{x.strftime('%M')}-{x.strftime('%S')}.avi"
        video_out = cv.VideoWriter(filename, fourcc, fps, (width, height))

        app.configure(fg_color="#131313")
        start_label = CTkLabel(app, text="Started Recording!", font=("Segoe UI", 18))
        start_label.place(relx=0.5, rely=0.05, anchor="n")
        app.after(1000, start_label.destroy)

        disable_buttons()
        video_button.configure(image=stop_icon, text='Stop')
        recording_start_time = time.time()

    else:
        
        if video_out is not None:
            video_out.release()
            video_out = None

        app.configure(fg_color="#222222")
        enable_buttons()
        video_button.configure(image=video_icon, text='Video', require_redraw=False)
        stop_label = CTkLabel(app, text="Stopped Recording!", font=("Segoe UI", 18))
        stop_label.place(relx=0.5, rely=0.05, anchor="n")
        app.after(1000, stop_label.destroy)

#---------------------------------MEDIAPIPE CONFIG-----------------------------------------

mp_face_detection = mp.solutions.face_detection # type: ignore
mp_drawing = mp.solutions.drawing_utils # type: ignore
face_detection = mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.5)

#---------------------------------TKINTER APP CONFIG----------------------------------------

app = CTk()
app.geometry('960x620')
app.title('Camera App')
app.configure(fg_color="#222222")

set_appearance_mode("dark")
set_widget_scaling(1)
app.resizable(False, False)
face_detection_textvar = StringVar(value='on')
is_flipped_textvar = StringVar(value='on')

#----------------------------------WIDGETS CONFIG-------------------------------------------------

# NORMAL IMAGES
my_font = CTkFont(family='Segoe UI', weight='bold', size=22)
camera_icon = CTkImage(light_image=Image.open("Assets/camera.png"), dark_image=Image.open("Assets/camera.png"), size=(50, 50))
video_icon = CTkImage(light_image=Image.open("Assets/video.png"), dark_image=Image.open("Assets/video.png"), size=(50, 50))
bw_icon = CTkImage(light_image=Image.open("Assets/bw.png"), dark_image=Image.open("Assets/bw.png"), size=(50, 50))
settings_icon = CTkImage(light_image=Image.open("Assets/settings.png"), dark_image=Image.open("Assets/settings.png"), size=(50, 50))
stop_icon = CTkImage(light_image=Image.open("Assets/stop.png"), dark_image=Image.open("Assets/stop.png"), size=(50, 50))

# DISABLED IMAGES
camera_icon_d = CTkImage(light_image=Image.open("Assets/camera_d.png"), dark_image=Image.open("Assets/camera_d.png"), size=(50, 50))
bw_icon_d = CTkImage(light_image=Image.open("Assets/bw_d.png"), dark_image=Image.open("Assets/bw_d.png"), size=(50, 50))
settings_icon_d = CTkImage(light_image=Image.open("Assets/settings_d.png"), dark_image=Image.open("Assets/settings_d.png"), size=(50, 50))

# CTK WIDGETS
buttons_frame = CTkFrame(app, fg_color='transparent', width=500, height=500)
photo_button = CTkButton(buttons_frame, text="Photo", hover=True, corner_radius=0, border_spacing=0, font=my_font, command=photo_button_click, border_color='red', image=camera_icon, fg_color='transparent', hover_color='#5e6470')
video_button = CTkButton(buttons_frame, text="Video", hover=True, corner_radius=0, border_spacing=0, font=my_font,command=video_button_clicked, border_color='red', image=video_icon, fg_color='transparent', hover_color='#5e6470')
bw_button = CTkButton(buttons_frame, text="B/W", hover=True, corner_radius=0, border_spacing=0, font=my_font, command=bw_button_click,  border_color='red', image=bw_icon, fg_color='transparent', hover_color='#5e6470')
settings_button = CTkButton(buttons_frame, text="Settings", hover=True, corner_radius=0, border_spacing=0,command=settings_button_click, font=my_font, border_color='red', image=settings_icon, fg_color='transparent', hover_color='#5e6470')
image_label = CTkLabel(app, text='')

#-----------------------------------OPENCV INIT------------------------------------------------------

webcam = cv.VideoCapture(0)
width = int(webcam.get(3))
height = int(webcam.get(4))
fourcc = cv.VideoWriter_fourcc(*'XVID') # type: ignore
fps = webcam.get(cv.CAP_PROP_FPS)

def update_webcam():
    
    global to_save_image

    success, frame = webcam.read()
    if not success:
        return
    width = int(webcam.get(3))
    height = int(webcam.get(4))


    if is_flipped:
        frame = cv.flip(frame, 1)
    if is_grayscale:
        frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        frame = cv.cvtColor(frame, cv.COLOR_GRAY2RGB)
    else:
        frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    
    photo_image = cv.cvtColor(frame, cv.COLOR_RGB2BGR)
    

    if is_face_detection:
        results = face_detection.process(frame)
        if results.detections:
            for detection in results.detections:
                bboxC = detection.location_data.relative_bounding_box
                ih, iw, _ = frame.shape
                x = int(bboxC.xmin * iw)
                y = int(bboxC.ymin * ih)
                w = int(bboxC.width * iw)
                h = int(bboxC.height * ih)

                cv.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 255), 1)
    
    pil_frame = Image.fromarray(frame)
    final_webcam_image = CTkImage(dark_image=pil_frame, size=(720, 500))
    

    if to_save_image:
        x = datetime.datetime.now()
        cv.imwrite(f"Photos/{x.strftime('%Y')}-{x.strftime('%H')}-{x.strftime('%M')}-{x.strftime('%S')}.jpg", photo_image)
        to_save_image = False

    if is_recording and video_out is not None:
        video_out.write(photo_image)



    image_label.configure(image=final_webcam_image)
    app.after(10, update_webcam)




#-----------------------PACKING WIDGETS---------------------------------

image_label.pack(padx=5, pady=15)
buttons_frame.pack()

photo_button.pack(in_=buttons_frame, side='left', padx=5, pady=5)
video_button.pack(in_=buttons_frame, side="left", padx=5, pady=5)
bw_button.pack(in_=buttons_frame, side="left", padx=5, pady=5)
settings_button.pack(in_=buttons_frame, side="left", padx=5, pady=5)

#-----------------------FINAL MAINLOOP------------------------------------

if __name__ == '__main__':
    update_webcam()
    app.mainloop()
    webcam.release()
