import sys
import pywinstyles
import customtkinter as ctk
import convertLink as cvl
from interface2.prefixes import *
from PIL import Image
import os
# import ctypes | no usage cause of solved problem






def keypress_handler(event): # The issue with pasting not working has been solved.
    if event.state & 0x4:  # Ctrl
        if event.keycode == 65:       # A
            event.widget.event_generate('<<SelectAll>>')
            return "break"
        elif event.keycode == 86:     # V
            event.widget.event_generate('<<Paste>>')
            return "break"
        elif event.keycode == 67:     # C
            event.widget.event_generate('<<Copy>>')
            return "break"
        elif event.keycode == 88:     # X
            event.widget.event_generate('<<Cut>>')
            return "break"
'''
def is_russian_layout():
    user32 = ctypes.WinDLL('user32')
    hwnd = user32.GetForegroundWindow()
    thread_id = user32.GetWindowThreadProcessId(hwnd, 0)
    lang_id = user32.GetKeyboardLayout(thread_id) & (2**16 - 1)
    return lang_id == 0x419

def update_layout_warning():
    if is_russian_layout():
        lbl_lng_warn.configure(text='!!! CTRL+V с раскладкой на русском языке не работает !!!')
    else:
        lbl_lng_warn.configure(text='')
    window.after(100, update_layout_warning)
'''
# FIXED WITH keypress_handler



def check_link(url_video, url_audio):
    cvl.url_video = entry_video.get()
    cvl.url_audio = entry_audio.get()
    video_found = False
    audio_found = False

    for word in domain_contains:
        if word in url_video:
            start_download_video(url_video)
            video_found = True
            break

    for word in domain_contains:
        if word in url_audio:
            start_download_audio(url_audio)
            audio_found = True
            break

    if not video_found and not audio_found:
        lbl_log.configure(text='Нужно ввести ссылку')




def start_download_video(url_video):
    cvl.link_to_video(url_video)


def start_download_audio(url_audio):
    cvl.link_to_audio(url_audio)


ctk.set_appearance_mode("dark")  # "light", "dark", "system"
ctk.set_default_color_theme("green")  # "blue", "dark-blue", "green"
ctk.set_window_scaling(2)



window = ctk.CTk()
window.title("Converter")
# window.iconbitmap(r"C:\Users\User\Downloads\canvas_copy-removebg-preview.ico")
window.resizable(False, False)

# cs of exe
base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
icon_path = os.path.join(base_path, "logo.ico")
window.iconbitmap(icon_path)


cvl.window = window

# BACKGROUND

image_path = os.path.join(base_path, "background.jpg")
img = Image.open(image_path)
bg_img = ctk.CTkImage(light_image=img, size=img.size)

label_bg = ctk.CTkLabel(window, image=bg_img, text="")
label_bg.place(x=0, y=0, relwidth=1, relheight=1)
label_bg.lower()






#########################

frame_inputs = ctk.CTkFrame(window)                                 # frame 1
frame_inputs.pack(fill="x", pady=10, padx=10)

label_video = ctk.CTkLabel(frame_inputs, text="Ссылка на видео:")
label_video.grid(row=0, column=0, sticky="w", padx=5, pady=5)

entry_video = ctk.CTkEntry(frame_inputs, width=600)
entry_video.grid(row=0, column=1, padx=5, pady=5)

label_audio = ctk.CTkLabel(frame_inputs, text="Ссылка на аудио:")
label_audio.grid(row=1, column=0, sticky="w", padx=5, pady=5)

entry_audio = ctk.CTkEntry(frame_inputs, width=600)
entry_audio.grid(row=1, column=1, padx=5, pady=5)

frame_progress = ctk.CTkFrame(window)                               # frame 2
frame_progress.pack(fill="x", pady=10, padx=10)


progress = ctk.CTkProgressBar(frame_progress)
progress.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky="ew")
progress.set(0)
cvl.progress = progress


lbl_log = ctk.CTkLabel(master=frame_progress, text=cvl.message, text_color='white')
lbl_log.grid(row=0, column=3)
cvl.lbl_log = lbl_log


frame_bottom = ctk.CTkFrame(window)                                # frame 3
frame_bottom.pack(fill="x", pady=10, padx=10)

btn_clear = ctk.CTkButton(frame_bottom, text="Очистить", fg_color="#a51313", command=lambda: (entry_video.delete(0, ctk.END), entry_audio.delete(0, ctk.END), lbl_log.configure(text='')))
btn_clear.grid(row=1, column=0, padx=10, pady=10)

btn_convert = ctk.CTkButton(frame_bottom, text="Конвертировать", command=lambda: check_link(entry_video.get(), entry_audio.get()))
btn_convert.grid(row=1, column=1, padx=10, pady=10)



'''
lbl_lng_warn = ctk.CTkLabel(frame_bottom, text='')
lbl_lng_warn.grid(row=1, column=2, padx=10, pady=10, columnspan=2)
'''
# FIXED WITH keypress_handler





# OPACITY FOR BG

pywinstyles.set_opacity(frame_inputs, value=0.6)
pywinstyles.set_opacity(frame_progress, value=0.8)
pywinstyles.set_opacity(frame_bottom, value=0.9)





for widget in [entry_video, entry_audio]:
    widget.bind('<KeyPress>', keypress_handler)




# update_layout_warning()

# FIXED WITH keypress_handler



window.mainloop()
