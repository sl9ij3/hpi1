from ultralytics import YOLO
import os
import shutil

model_path = input("Enter model path (default='yolov8n.pt'): ")
if not model_path:
    model_path = 'yolov8n.pt'

save_dir = input("Enter save directory (default='predictions/'): ")
if not save_dir:
    save_dir = 'predictions/'
if not os.path.isdir(save_dir):
    os.makedirs(save_dir)

images_path = input("Enter images path (default='datasets/test/'): ")
if not images_path:
    images_path = 'datasets/test/'
if not os.path.isdir(images_path):
    print(images_path, "does not exist")
    exit()
if not os.listdir(images_path):
    print(images_path, "there is no images to predict")
    exit()


move_images = input("Move images to predict directory? (Y/N, default='N'): ").upper()
if move_images not in ['Y', 'N']:
    move_images = 'N'


model = YOLO(model_path)

images = [f for f in os.listdir(images_path) if f.endswith(('.jpg', '.jpeg', '.png'))]

if move_images == 'Y':
    predict_dir = os.path.join(save_dir, "predict")
    if os.path.isdir(predict_dir):
        if not os.path.isdir(os.path.join(save_dir, "predict2")):
            predict_dir = os.path.join(save_dir, "predict2")
        else:
            predict_folders = [f for f in os.listdir(save_dir) if f.startswith('predict') and len(f) > 7]
            predict_nums = [int(f[7:]) for f in predict_folders]
            next_predict_num = max(predict_nums) + 1
            predict_dir = os.path.join(save_dir, "predict" + str(next_predict_num))
    images_dir = os.path.join(predict_dir, 'images')

for image in images:
    model.predict(source=os.path.join(images_path, image), project=save_dir, save_txt=True, save_conf=False)
    if move_images == 'Y':
        if not os.path.isdir(images_dir):
            os.makedirs(images_dir)
        shutil.move(os.path.join(images_path, image), os.path.join(images_dir, image))

