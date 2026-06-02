import common
from tqdm import tqdm
import random
import hq_anomaly.common
import hq_anomaly.models
import sys
import numpy as np
import cv2
import shutil
import os


if __name__=="__main__":
    records = common.get_records("2026-05-29 00:00:00", "2026-05-30 00:00:00", position="正面")
    threshold = 0.5
    
    ckpt_path = sys.argv[1]
    output_path = sys.argv[2]

    model_config = hq_anomaly.common.ModelConfig(
        checkpoint_path=ckpt_path,
    )
    model = hq_anomaly.models.ViTPatchcore(model_config)

    model.eval()

    image_paths = []
    for rec in tqdm(records):
        image_path = rec["local_pic_url"]
        way_point_id = rec["way_point_id"]
        if way_point_id is None:
            continue

        way_point = int(way_point_id.split("_")[2])

        if way_point <= 25:
            image_paths.append(image_path)
            pass
        pass

    print(len(image_paths))
    random.shuffle(image_paths)

    bar = tqdm(image_paths)
    for image_path in bar:
        img = cv2.imdecode(np.fromfile(image_path, dtype=np.int8), -1)
        result = model.predict([img], return_heatmap=True)[0]
        bar.set_postfix({"score": result.score.max()})
        if result.score.max() > threshold:
            print(image_path)
            raw_name = os.path.basename(image_path)
            idname, _ = os.path.splitext(raw_name)
            heatmap_name = idname + "_heatmap.jpg"
            cv2.imencode(".jpg", result.heat_map)[1].tofile(os.path.join(output_path, heatmap_name))
            shutil.copy(image_path, os.path.join(output_path, raw_name))
            pass
        pass
    pass