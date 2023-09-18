#!/usr/bin/env python
# coding: utf-8

import dtlpy as dl

if dl.token_expired():
    dl.login()

project = dl.projects.get(project_name='My-Project')

dataset = project.datasets.get(dataset_name='My-Dataset')


my_filter = dl.Filters(resource=dl.FiltersResource.ANNOTATION)
my_filter.add(field='type', values='point')
pages = dataset.items.list(filters=my_filter)

for item in pages.all():
    print('\n')
    print("Item ID: {}, Item Name: {}".format(item.item.id,item.item.name))
    print("Annotation ID: {}, Annotation Label: {}".format(item.id,item.label))
    x = list(item.coordinates.values())[:2][0]
    y = list(item.coordinates.values())[:2][1]
    print("Annotation Position: ({}, {})".format(x, y))

