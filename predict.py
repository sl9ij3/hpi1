from ultralytics import YOLO
import os
import shutil

def_model = 'yolov8n.pt'

predict_folders = [f for f in os.listdir('runs/detect/') if f.startswith('train') and len(f) > 5]
if len(predict_folders) > 1:
    predict_nums = [int(f[5:]) for f in predict_folders]
    next_predict_num = max(predict_nums)
    for num in predict_nums[::-1]:
        model_dir = 'runs/detect/train' + str(num) + '/weights/best.pt'
        if os.path.exists(model_dir):
            def_model = model_dir
            break
        else:
            print(model_dir, 'does not exist')
elif os.path.exists('runs/detect/train/weights/best.pt'):
    def_model = 'runs/detect/train/weights/best.pt'

model_path = input(f"Enter model path (default='{def_model}'): ")
if not model_path:
    model_path = def_model

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


images_action = input("Copy[C] / Move[M] images to predict directory? (M/C, default='N'): ").upper()
if images_action not in ['C', 'M', 'N']:
    images_action = 'N'

model = YOLO(model_path)

images = [f for f in os.listdir(images_path) if f.endswith(('.jpg', '.jpeg', '.png'))]

if images_action != 'Y':
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
    if images_action == 'M':
        if not os.path.isdir(images_dir):
            os.makedirs(images_dir)
        shutil.move(os.path.join(images_path, image), os.path.join(images_dir, image))
    elif images_action == 'C':
        if not os.path.isdir(images_dir):
            os.makedirs(images_dir)
        shutil.copy(os.path.join(images_path, image), os.path.join(images_dir, image))

