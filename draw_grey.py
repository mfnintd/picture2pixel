import json
import numpy as np
import cv2 as cv

def import_and_color(path_to_json):
    data = json.load(open(path_to_json))
    #print(data)
    h, w = data["height"], data["width"]

    color_list = [
        (x['b'], x['g'], x['r']) for x in data["color_origin"]
    ]
    print(color_list)
    board = [row for row in data["data"]]
    #print(board)
    output_img = np.zeros((h, w, 3))
    for i in range(h):
        for j in range(w):
            #print(color_list[board[i][j]])
            #print(board[i][j])
            output_img[i][j] = np.array(color_list[board[i][j]])
    # for region in data["map"]:
    #     #region hiện là dict của 1 vùng
        
    #     color = np.array(list(region["gray"].values()))
        
    #     #for point in region["p"]:
    #     #    output_img[point[0]][point[1]] = color
    #     for i in region["points"]:
    #         output_img[i // w][i % w] = color
    cv.imwrite("draw_gray.png", output_img)

if __name__ == "__main__":
    #img = cv.imread("color_quantiztion_2.png")
    import_and_color("color_map.json")
    print("done")
    pass