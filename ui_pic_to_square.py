import json
import random
import tkinter as tk
from tkinter import Label, Entry, Button, StringVar, ttk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2
import os

import numpy as np


def show_origin_image():
    label_loading.config(text='Processing',fg='#f00')
    root.update()
    path = entry_image_path.get()

    if path == None or path == '':
        return
    img = Image.open(path)
    w, h = img.size
    w, h = 392, int(392 / w * h)
    
    if h > 392:
        w, h = int(392 / h * w), 392
    print(w, h)
    img = img.resize((w, h), Image.Resampling.NEAREST)
    imgtk = ImageTk.PhotoImage(img)
    label_origin_image.imgtk = imgtk
    label_origin_image.configure(image=imgtk)
    label_loading.config(text='Done!',fg='#0f0')

def show_gray_image():
    label_loading.config(text='Processing',fg='#f00')
    root.update()
    #global resized_img
    img = cv2.cvtColor(resized_img, cv2.COLOR_BGR2GRAY)   
    img = Image.fromarray(cv2.cvtColor(resized_img, cv2.COLOR_BGR2GRAY))
    
    w, h = img.size
    w, h = 392, int(392 / w * h)
    
    if h > 392:
        w, h = int(392 / h * w), 392
    print(w, h, color_num)

    img = img.resize((w, h), Image.Resampling.NEAREST)
    imgtk = ImageTk.PhotoImage(img)
    label_gray_image.imgtk = imgtk
    label_gray_image.configure(image=imgtk)
    label_loading.config(text='Done!',fg='#0f0')

def show_resized_image():
    label_loading.config(text='Processing',fg='#f00')
    root.update()

    #La cai de luu
    global resized_img, color_num
    path = entry_image_path.get()
    color_num = combo_color_number.get()
    print(color_num)
    new_width = combo_width_size.get()

    if path == None or path == '' or color_num == None or color_num == '' or new_width == None or new_width == '':
        #label_resized_image.after(10)
        return
    
    color_num = int(color_num)
    new_width = int(new_width)
    img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    color_list = dict()

    is_tranparent = False
    if img.shape[2] == 4:
        trans_mark = img[:, :, 3] == 0
        img[trans_mark] = [255, 255, 255, 255]
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        is_tranparent = True

    h, w, _ = img.shape
    new_height = new_width * h // w
    resized_img = cv2.resize(img, (new_width, new_height), interpolation = cv2.INTER_NEAREST_EXACT)

    
    for _ in resized_img:
        for pixel in _:
            color_here = (int(pixel[0]), int(pixel[1]), int(pixel[2]))
        #if (pixel[3] > 100):
            color_list[color_here] = 1 if not color_here in color_list else color_list[color_here] + 1
    
    color_num = min(color_num, len(color_list))
    combo_color_number.set(color_num)

    def top_k_color(count_dict, k):
        # Sắp xếp các mục trong dictionary theo giá trị giảm dần
        sorted_items = sorted(count_dict.items(), key=lambda item: item[1], reverse=True)
        # Lấy ra k mục đầu tiên
        top_k_items = sorted_items[:k]
        # Trả về danh sách các chuỗi (keys) tương ứng với các mục đã chọn
        return [item[0] for item in top_k_items]
    #TODO
    #color_list_aft = top_k_color(color_list, color_num)
    color_list_aft = random.sample(list(color_list), k=color_num)
    if is_tranparent:
        color_list_aft[-1] = (255, 255, 255)


    color_map = {}
    #data = []

    for row in range(new_height):
        #data_row = []
        for col in range(new_width):
            # if resized_img[row][col][3] <= 100:
            #     resized_img[row][col] = np.array((255, 255, 255))
            # else:
            color = (resized_img[row][col][0], resized_img[row][col][1], resized_img[row][col][2])

            distance = [np.sqrt(sum([(color[j] - color_list_aft[i][j]) ** 2 for j in range(3)])) for i in range(color_num)]
            #print(distance)
            #data_row.append(int(np.argmin(distance)))
            tmp = color_list_aft[int(np.argmin(distance))]

            resized_img[row][col] = np.array(tmp)
            
            if not tmp in color_map:
                color_map[tmp] = []
            color_map[tmp].append((row, col))
        #data.append(data_row)

    img = Image.fromarray(cv2.cvtColor(resized_img, cv2.COLOR_BGR2RGB))
    
    w, h = img.size
    w, h = 392, int(392 / w * h)
    
    if h > 392:
        w, h = int(392 / h * w), 392
    print(w, h, color_num)

    img = img.resize((w, h), Image.Resampling.NEAREST)
    imgtk = ImageTk.PhotoImage(img)
    label_resized_image.imgtk = imgtk
    label_resized_image.configure(image=imgtk)
    
    #label_resized_image.after(10)
    show_gray_image()
    label_loading.config(text='Done!',fg='#0f0')
    


#ui
#main window
root = tk.Tk()
root.title("Resize UI")
root.geometry("1500x800")

#ảnh gốc
label_origin_image = Label(root)
label_origin_image.place(x=75, y=70, width=392, height=392)

#ảnh resized
label_resized_image = Label(root)
label_resized_image.place(x=549, y=70, width=392, height=392)


#ảnh resized
label_gray_image = Label(root)
label_gray_image.place(x=1031, y=70, width=392, height=392)


def browse_files():
    label_loading.config(text='Processing',fg='#f00')
    root.update()
    filename = filedialog.askopenfilename(initialdir="/" if entry_image_path.get() == '' else entry_image_path.get(), title="Select an Image",
        filetypes=(("IMAGE", ["*.png*", "*.jpg*", "*.jpeg*", "*.webp*"]), ("all files", "*.*")))
    return filename

def browse_folder():
    label_loading.config(text='Processing',fg='#f00')
    root.update()
    foldername = filedialog.askdirectory(initialdir="/" if entry_output_path.get() == '' else entry_output_path.get(), title="Select folder output")

def set_entry_image_path():
    label_loading.config(text='Processing',fg='#f00')
    root.update()
    val = browse_files()
    entry_image_path.delete(0, tk.END)
    entry_image_path.insert(0, val)    
    set_output_path('/'.join(val.split('/')[:-1]) + '/')
    show_origin_image()
    show_resized_image()

def set_output_path(val):
    label_loading.config(text='Processing',fg='#f00')
    root.update()
    #val = browse_folder()
    entry_output_path.delete(0, tk.END)
    entry_output_path.insert(0, val)

def show_with_event(event):
    label_loading.config(text='Processing',fg='#f00')
    root.update()
    show_resized_image()

#Đường dẫn file ảnh
label_image_path = Label(root, text="Image Path:")
label_image_path.place(x=75, y=502)
entry_image_path = Entry(root)
entry_image_path.place(x=167, y=502, width=400)
#nút browser
btn_browser_image_path = Button(root, text="Browser", command=set_entry_image_path)
btn_browser_image_path.place(x=563, y=502)

#Đường dẫn thư mục đầu ra
label_output_path = Label(root, text="Output folder:")
label_output_path.place(x=75, y=596)
entry_output_path = Entry(root)
entry_output_path.place(x=167, y=596, width=400)
#nút browser
btn_browser_output_path = Button(root, text="Browser", command=lambda:set_output_path(browse_folder()))
btn_browser_output_path.place(x=563, y=596)

#Số lượng màu
label_color_number = Label(root, text="Number of Color:")
label_color_number.place(x=795, y=502)
combo_color_number = ttk.Combobox(
   values=[str(i) for i in range(10, 201, 10)]
   )

combo_color_number.current(0)
combo_color_number.place(x=969, y=502)
combo_color_number.bind("<<ComboboxSelected>>", show_with_event)

#Số pixel ngang
label_width_size = Label(root, text="Width size:")
label_width_size.place(x=795, y=596)
combo_width_size = ttk.Combobox(
   values=[str(i) for i in range(10, 501, 10)]
   )
combo_width_size.current(0)
combo_width_size.place(x=969, y=596)
combo_width_size.bind("<<ComboboxSelected>>", show_with_event)


btn_reconvert = Button(root, text="re-convert", command=show_resized_image) #TODO command = ?
btn_reconvert.place(x=1211, y=502)

def export():

    label_loading.config(text='Processing',fg='#f00')
    root.update()
    
    global resized_img, color_num
    h, w, _ = resized_img.shape

    color_origin = []
    data = []
    for row in range(h):
        row_data = []
        for col in range(w):
            tmp = resized_img[row][col]
            color_here = (tmp[2], tmp[1], tmp[0])
            if not color_here in color_origin:
                color_origin.append(color_here)
            row_data.append(color_origin.index(color_here))
        data.append(row_data)

    json_content = {
        "height": h,
        "width": w,
        "color_num": color_num,
        "color_origin": [
            {
                "r": int(area[0]),
                "g": int(area[1]),
                "b": int(area[2])
            }
            for area in color_origin
        ],
        "color_gray": [
            {
                "r": int(sum(area) / 3 * 11 / 10),
                "g": int(sum(area) / 3 * 11 / 10),
                "b": int(sum(area) / 3 * 11 / 10)
            }
            for area in color_origin
        ],
        "data": [val for val in data]
    }

    json_output = entry_output_path.get() + 'json_output/'
    image_output = entry_output_path.get()+ 'image_output/'

    if not os.path.exists(json_output):
        os.makedirs(json_output)
    if not os.path.exists(image_output):
        os.makedirs(image_output)
    #print(json_output + os.path.basename(entry_image_path).split('.')[0] + '_' + str(color_num) + '_' + str(h) + 'x' + str(w) + '.json')
    
    with open(json_output + os.path.basename(entry_image_path.get()).split('.')[0] + '_' + str(color_num) + '_' + str(h) + 'x' + str(w) + '.json', "w") as outfile:
        json.dump(json_content, outfile, separators=(',', ':'))
    
    cv2.imwrite(image_output + os.path.basename(entry_image_path.get()).split('.')[0] + '_' + str(color_num) + '_' + str(h) + 'x' + str(w) + '.png', resized_img)
    
    label_loading.config(text='Done!',fg='#0f0')
    
#Nút bấm xuất
btn_export = Button(root, text="Export", command=export)
btn_export.place(x=1211, y=596)


#loading
label_loading = Label(root)
label_loading.place(x=669, y=669)
label_loading.config(font=20)

root.mainloop()