import json
import cv2 as cv
import random
import numpy as np
import math

color_num = 40
input = 'tulip.png'
new_height = int
new_width = 100

def covert_to_pixel_style(img, color_num, new_width, output_name):
    #print(img)
    #global new_height, new_width, color_num
    #print(img.shape())
    h, w, _ = img.shape
    new_height = new_width * h // w
    resize_img = cv.resize(img, (new_width, new_height),interpolation = cv.INTER_NEAREST_EXACT)
    
    json_result = {}
    color_map = {}

    #cv.imwrite('resize.png', resize_img)

    color_list = dict()
    for _ in resize_img:
        for pixel in _:
            color_here = (int(pixel[0]), int(pixel[1]), int(pixel[2]))
            color_list[color_here] = 1 if not color_here in color_list else color_list[color_here] + 1
    
    #print(list(color_list))
    
    color_num = min(color_num, len(color_list))

    #print(color_num)
    #color_list_aft = sorted(list(color_list), key=color_list[1])[:color_num]

    #color_list_aft = max()
    #print(color_list.keys())
    color_list_aft = random.sample(list(color_list), k=color_num)

    data = []

    #print(resize_img[0][20])
    for row in range(new_height):
        data_row = []
        for col in range(new_width):
            
            color = (resize_img[row][col][0], resize_img[row][col][1], resize_img[row][col][2])

            distance = [np.sqrt(sum([(color[j] - color_list_aft[i][j]) ** 2 for j in range(3)])) for i in range(color_num)]
            #print(distance)
            data_row.append(int(np.argmin(distance)))
            tmp = color_list_aft[data_row[-1]]

            resize_img[row][col] = np.array(tmp)
            
            if not tmp in color_map:
                color_map[tmp] = []
            color_map[tmp].append((row, col))
        data.append(data_row)

    cv.imwrite(output_name + '_' + color_num + '_' + str(new_height) + 'x' + str(new_width) + '.png', resize_img)
    
    img_gray = cv.cvtColor(resize_img, cv.COLOR_BGR2GRAY)
    #cv.imwrite('gray.png', img_gray)

    json_result = {
        "height": new_height,
        "width": new_width,
        "color_num": color_num,
        "color_origin": [
            {
                "r": area[2],
                "g": area[1],
                "b": area[0]
            }   
            for area in color_list_aft
        ],
        "color_gray": [
            {
                "b": int(sum(area)/3),
                "g": int(sum(area)/3),
                "r": int(sum(area)/3)
            }
            for area in color_list_aft
        ],
        "data": [val for val in data]
    }
    
    with open(output_name + '_' + color_num + '_' + + str(new_height) + 'x' + str(new_width) + '.json', "w") as outfile: 
        json.dump(json_result, outfile, separators=(',', ':'))

if __name__ == "__main__":
    img = cv.imread(input)
    #img = cv.imread("color_quantiztion_2.png")
    covert_to_pixel_style(img, color_num, new_width)
    pass