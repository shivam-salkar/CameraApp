from customtkinter import * # type: ignore
from PIL import Image
import PIL
import cv2 as cv
import datetime
import mediapipe as mp
import os
os.makedirs("Photos", exist_ok=True)

#--------------------FUNCTIONS----------------------

to_save_image = False
is_grayscale = False
settings_window = None
is_face_detection = True


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
    if settings_window == None or not settings_window.winfo_exists():
        settings_window = CTkToplevel()
        settings_window.geometry('500x500')
        settings_window.title('Settings')
        
        face_detection_textvar = StringVar(value='on')
        face_detection_checkbox = CTkCheckBox(settings_window, text="Face Detection", command=is_face_detection_checkbox, onvalue="on", offvalue="off", variable=face_detection_textvar)
        face_detection_checkbox.pack()



        settings_window.focus()
    else:
        settings_window.focus()
    

def is_face_detection_checkbox():
    global is_face_detection
    if is_face_detection:
        is_face_detection = False
    else:
        is_face_detection = True

#---------------------------------MEDIAPIPE CONFIG-----------------------------------------

mp_face_detection = mp.solutions.face_detection # type: ignore
mp_drawing = mp.solutions.drawing_utils # type: ignore
face_detection = mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.5)

#---------------------------------TKINTER APP CONFIG----------------------------------------

app = CTk()
app.geometry('960x620')
app.title('Camera App')
set_appearance_mode("dark")
set_widget_scaling(1)
app.resizable(False, False)



#----------------------------------WIDGETS CONFIG-------------------------------------------------

my_font = CTkFont(family='Segoe UI', weight='bold', size=22)
camera_icon = CTkImage(light_image=Image.open("Assets/camera.png"), dark_image=Image.open("Assets/camera.png"), size=(50, 50))
video_icon = CTkImage(light_image=Image.open("Assets/video.png"), dark_image=Image.open("Assets/video.png"), size=(50, 50))
bw_icon = CTkImage(light_image=Image.open("Assets/bw.png"), dark_image=Image.open("Assets/bw.png"), size=(50, 50))
settings_icon = CTkImage(light_image=Image.open("Assets/settings.png"), dark_image=Image.open("Assets/settings.png"), size=(50, 50))

buttons_frame = CTkFrame(app, fg_color='transparent', width=500, height=500)
photo_button = CTkButton(buttons_frame, text="Photo", hover=True, corner_radius=0, border_spacing=0, font=my_font, command=photo_button_click, border_color='red', image=camera_icon, fg_color='transparent', hover_color='#5e6470')
video_button = CTkButton(buttons_frame, text="Video", hover=True, corner_radius=0, border_spacing=0, font=my_font, border_color='red', image=video_icon, fg_color='transparent', hover_color='#5e6470')
bw_button = CTkButton(buttons_frame, text="B/W", hover=True, corner_radius=0, border_spacing=0, font=my_font, command=bw_button_click,  border_color='red', image=bw_icon, fg_color='transparent', hover_color='#5e6470')
settings_button = CTkButton(buttons_frame, text="Settings", hover=True, corner_radius=0, border_spacing=0,command=settings_button_click, font=my_font, border_color='red', image=settings_icon, fg_color='transparent', hover_color='#5e6470')
image_label = CTkLabel(app, text='')


#-----------------------------------OPENCV INIT------------------------------------------------------

webcam = cv.VideoCapture(0)


def update_webcam():
    global to_save_image

    success, frame = webcam.read()
    if not success:
        return

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

update_webcam()
app.mainloop()
webcam.release()
