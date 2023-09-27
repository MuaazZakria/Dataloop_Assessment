#!/usr/bin/env python
# coding: utf-8


######Import Libraries######

import dtlpy as dl
from datetime import datetime
import json

######Login to Dataloop######

if dl.token_expired():
    dl.login()
    
######Creating / getting the project & dataset######

try:
    project = dl.projects.get(project_name='My-Project')
    dataset = project.datasets.get(dataset_name='My-Dataset')
except:
    project = dl.projects.create(project_name='My-Project')
    project = dl.projects.get(project_name='My-Project')
    dataset = project.datasets.create(dataset_name='My-Dataset')
    dataset = project.datasets.get(dataset_name='My-Dataset')

######Uploading the images by adding UTM metadata######

local_path = [r"C:\Users\DELL\ML Solution Engineering Home Assignment\images"]

# Get the current Unix timestamp
timestamp = int(datetime.utcnow().timestamp())

item_metadata = {'user': {'collected': timestamp}}

dataset.items.upload(local_path=local_path,
                     item_metadata=item_metadata)

######Adding the labels######

dataset.add_labels(label_list=['1', '2', '3', 'top', 'bottom'])


######Uploading the annotations######

with open(r'C:\\Users\\DELL\\ML Solution Engineering Home Assignment\ML Solution Engineering Home Assignment.json', 'r') as f:
    data = json.load(f)
    
pages = dataset.items.list()
for item in pages.all():
    builder = item.annotations.builder()

    for annotation_data in data[item.name]:
        label = annotation_data['label']
        confidence = annotation_data['confidence']

        if 'point' in annotation_data:
            point_data = annotation_data['point']
            x = point_data['x']
            y = point_data['y']
            builder.add(annotation_definition=dl.Point(x=x, y=y, label=label),
                            model_info={'name': 'confidence', 'confidence': confidence})

        elif 'box' in annotation_data:
            box_data = annotation_data['box']
            x1, y1 = box_data[0]['x'], box_data[0]['y']
            x2, y2 = box_data[1]['x'], box_data[1]['y']
            builder.add(annotation_definition=dl.Box(top=y1, left=x1, bottom=y2, right=x2, label=label),
                            model_info={'name': 'confidence', 'confidence': confidence})

        elif 'polygon' in annotation_data:
            polygon_coordinates = annotation_data['polygon']

            builder.add(annotation_definition=dl.Polygon(geo=polygon_coordinates, label=label),
                            model_info={'name': 'confidence', 'confidence': confidence})

        try:
            item.annotations.upload(builder)
        except:
            pass
