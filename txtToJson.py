import os
import json
import argparse

parser = argparse.ArgumentParser(description='Convert annotations from TXT to JSON format')
parser.add_argument('input_dir', type=str, help='input directory containing TXT files')
parser.add_argument('output_dir', type=str, help='output directory for JSON files')
args = parser.parse_args()

input_dir = args.input_dir
output_dir = args.output_dir

for txt_file in [f for f in os.listdir(input_dir) if f.endswith('.txt') and f != 'classes.txt']:
    with open(os.path.join(input_dir, txt_file), "r") as f:
        annotations = []
        for line in f:
            values = line.split()
            label = values[0]
            x1 = float(values[1])
            y1 = float(values[2])
            x2 = float(values[3])
            y2 = float(values[4])
            width = x2 - x1
            height = y2 - y1
            annotation = {
                "label": label,
                "xmin": x1,
                "ymin": y1,
                "xmax": x2,
                "ymax": y2
            }
            annotations.append(annotation)
        output_file = os.path.splitext(txt_file)[0] + ".json"
        output_path = os.path.join(output_dir, output_file)
        with open(output_path, "w") as f:
            json.dump(annotations, f)
