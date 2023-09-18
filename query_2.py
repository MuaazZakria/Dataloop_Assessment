#!/usr/bin/env python
# coding: utf-8

import dtlpy as dl

if dl.token_expired():
    dl.login()

project = dl.projects.get(project_name='My-Project')

dataset = project.datasets.get(dataset_name='My-Dataset')


my_filter = dl.Filters()
my_filter.add_join(field='type', values='point')
pages = dataset.items.list(filters=my_filter)

for item in pages.all():
    print('\n')
    print("Item ID: {}, Item Name: {}".format(item.id,item.name))
    for annotation in item.annotations.list():
        print('Coordinates:')
        print(annotation.coordinates)

