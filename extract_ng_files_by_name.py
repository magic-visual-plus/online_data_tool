import os
import sqlalchemy
from sqlalchemy import create_engine, text
import ml_backend

import sys
import json
from copy import deepcopy
import uuid
import sys
import shutil
import numpy as np
from tqdm import tqdm
import time
import cv2
from PIL import Image, ImageFont, ImageDraw


FONT_PATH=os.path.join('..', 'simsun.ttc')

def putTextChinese(img, text, position, font_size, font_color):
    cv2_im_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    pil_im = Image.fromarray(cv2_im_rgb)
    font = ImageFont.truetype(FONT_PATH, font_size)
    draw = ImageDraw.Draw(pil_im)

    draw.text(position, text, font=font, fill=font_color)
    cv2_im = cv2.cvtColor(np.array(pil_im), cv2.COLOR_RGB2BGR)
    return cv2_im



if __name__ == '__main__':
    output_path = "e:\\imgs_defect"
    date = sys.argv[1]
    target_name = sys.argv[2]
    sql_url = 'mysql+mysqldb://root:12345678@127.0.0.1:3306/vision_backend'
    start_date = f'{date} 00:00:00'
    end_date = f'{date} 23:59:59'

    engine = sqlalchemy.create_engine(sql_url, poolclass=sqlalchemy.pool.NullPool)
    connection = engine.connect()

    # Select
    result = connection.execute(text(
        f'select local_pic_url, ng_result_uuid from product_detection_detail_result where check_status=1 and c_time between "{start_date}" and "{end_date}"'))
    
    updates = dict()
    
    output_path = os.path.join(output_path, date, target_name)
    
    os.makedirs(os.path.join(output_path, 'labeled'), exist_ok=True)
    os.makedirs(os.path.join(output_path, 'raw'), exist_ok=True)
    
    for row in tqdm(result.fetchall()):
        image_path = row[0]
        rid = row[1]
        
        parts = image_path.split('/')
        xinghao = parts[-6]
        id = parts[-4]
        # output_folder = os.path.join(output_path, xinghao, id)
        # if not os.path.exists(output_folder):
        #     os.makedirs(output_folder, exist_ok=True)
        #     time.sleep(0.1)
        #     pass

        defect_result = connection.execute(text(
            f'select defect_result from product_detection_ng_result where product_detail_id="{rid}" and defect_type="{target_name}"'
        )).fetchall()
        
        if len(defect_result) == 0:
            continue
        
        # img = cv2.imread(image_path)
        img = cv2.imdecode(np.fromfile(image_path, dtype=np.int8), -1)
        cnt = 0
        target = [target_name]
        for row in defect_result:
            rj = json.loads(row[0])
            name = rj['name']
            conf = rj['confidence']
            # if False:
            # print(name)
            if not any([t in name for t in target]):
                continue
            cnt += 1
            points = rj['points'][0]
            x = int(points['x'])
            y = int(points['y'])
            h = int(points['h'])
            w = int(points['w'])
            img = cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
            showtext = f"{name}: {conf:.2f}, {w}x{h}"
            img = putTextChinese(img, showtext, (x, y-60), 50, (255, 0, 0))
            pass
        
        if cnt == 0:
            continue
        
        output_filename = os.path.join(output_path, 'labeled', parts[-1])
        # cv2.imwrite(output_filename, img)
        cv2.imencode(".jpg", img)[1].tofile(output_filename)
        shutil.copy(image_path, os.path.join(output_path, 'raw', parts[-1]))
        pass
    
    connection.close()
    engine.dispose()
    pass
