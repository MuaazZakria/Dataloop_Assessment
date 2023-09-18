#!/usr/bin/env python
# coding: utf-8


#Import Libraries

import dtlpy as dl
from datetime import datetime
import json

#Login to Dataloop

if dl.token_expired():
    dl.login()
    
#Creating and getting the project

project = dl.projects.create(project_name='My-Project')    

project = dl.projects.get(project_name='My-Project')

#Creating and getting the dataset

dataset = project.datasets.create(dataset_name='My-Dataset')

dataset = project.datasets.get(dataset_name='My-Dataset')

#Uploading the images

local_path = [r"C:\Users\DELL\ML Solution Engineering Home Assignment\1.jpg",
              r"C:\Users\DELL\ML Solution Engineering Home Assignment\2.jpg",
              r"C:\Users\DELL\ML Solution Engineering Home Assignment\3.jpg"]

dataset = project.datasets.get(dataset_name='My-Dataset')
dataset.items.upload(local_path=local_path)

#Adding the labels

dataset.add_label(label_name='1')
dataset.add_label(label_name='2')
dataset.add_label(label_name='3')
dataset.add_label(label_name='top')
dataset.add_label(label_name='bottom')

#Adding UTM metadata

# Get the current Unix timestamp
timestamp = int(datetime.utcnow().timestamp())

filters = dl.Filters()

dataset.items.update(filters = filters, update_values={'user': {'collected': timestamp}})


#Uploading the annotations

with open(r'C:\\Users\\DELL\\ML Solution Engineering Home Assignment\ML Solution Engineering Home Assignment.json', 'r') as f:
    data = json.load(f)


data_1 = data['1.jpg']
data_2 = data['2.jpg']
data_3 = data['3.jpg']

#Image 1
item_1 = dataset.items.get(item_id='6507ad874baf20606c37960b')
builder = item_1.annotations.builder()
builder.add(annotation_definition=dl.Point(x=data_1[1]['point']['x'], y=data_1[1]['point']['y'], 
                                          label=data_1[1]['label']))

builder.add(annotation_definition=dl.Box(top=data_1[0]['box'][0]['y'],
                                         left=data_1[0]['box'][0]['x'],
                                         bottom=data_1[0]['box'][1]['x'],
                                         right=data_1[0]['box'][1]['y'],
                                         label=data_1[0]['label']))
builder.add(annotation_definition=dl.Point(x=data_1[2]['point']['x'], y=data_1[2]['point']['y'], 
                                          label=data_1[2]['label']))

polygon_coordinates = list(map(lambda point: [point['x'], point['y']], data_1[3]['polygon'][0]))

builder.add(annotation_definition=dl.Polygon(geo=polygon_coordinates,
                                             label=data_1[3]['label']))
item_1.annotations.upload(builder)

#Image 2
item_2 = dataset.items.get(item_id='6507ad8737f28628687ddc99')
builder = item_2.annotations.builder()
builder.add(annotation_definition=dl.Box(top=data_2[0]['box'][0]['y'],
                                         left=data_2[0]['box'][0]['x'],
                                         bottom=data_2[0]['box'][1]['x'],
                                         right=data_2[0]['box'][1]['y'],
                                         label=data_2[0]['label']))

item_2.annotations.upload(builder)

#Image 3
item_3 = dataset.items.get(item_id='6507ad8737f286a6867ddc95')
builder = item_3.annotations.builder()
builder.add(annotation_definition=dl.Point(x=data_3[0]['point']['x'], y=data_3[0]['point']['y'], 
                                          label=data_3[0]['label']))

builder.add(annotation_definition=dl.Point(x=data_3[1]['point']['x'], y=data_3[1]['point']['y'], 
                                          label=data_3[1]['label']))

item_3.annotations.upload(builder)