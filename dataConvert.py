import argparse
import json
import numpy as np
import pandas as pd

parser = argparse.ArgumentParser(description='file name')
parser.add_argument('-f', type=str, help='file to convert')
args = parser.parse_args()

filename = args.f

if filename == None:
    raise Exception('No file added. Use flag -f with csv file in same directory')

data = pd.read_csv(filename)

## iterate through responses and then interate through each task in a response 
def decode(annotation):
    reg_x = np.nan
    reg_y = np.nan
    solar_prom_x = np.nan
    solar_prom_y = np.nan
    solar_prom_x1 = np.nan
    solar_prom_y1 = np.nan
    solar_prom_x2 = np.nan
    solar_prom_y2 = np.nan
    solar_prom_x3 = np.nan
    solar_prom_y3 = np.nan
    solar_prom_x4 = np.nan
    solar_prom_y4 = np.nan
    reg_vis = np.nan
    prom_vis = np.nan
    cloud = np.nan
    any_else = np.nan
    
    for task in annotation:
        ## what do you see in this image
        if task['task'] == 'T0':
            class_img = task['value']

        ## are there clouds in this image
        elif task['task'] == 'T1':
            cloud = task['value']

        ## is regulus visible
        elif task['task'] == 'T2':
            reg_vis = task['value']

        ## anything else in this image? (catchall)
        elif task['task'] == 'T3':
            any_else = task['value']

        ## regulus coords
        elif task['task'] == 'T4':
            try:
                reg_x = task['value'][0]['x']
                reg_y = task['value'][0]['y']
            except IndexError:
                pass

        ## are solar prominences visible
        elif task['task'] == 'T5':
            prom_vis = task['value']

        ## circle solar prominences
        elif task['task'] == 'T6':
            for i in range(len(task['value'])):
                coords = task['value'][i]
                if i == 0:
                    solar_prom_x = coords['x']
                    solar_prom_y = coords['y']
                if i == 1:
                    solar_prom_x1 = coords['x']
                    solar_prom_y1 = coords['y']
                if i == 2:
                    solar_prom_x2 = coords['x']
                    solar_prom_y2 = coords['y']
                if i == 3:
                    solar_prom_x3 = coords['x']
                    solar_prom_y3 = coords['y']
                if i == 4:
                    solar_prom_x4 = coords['x']
                    solar_prom_y4 = coords['y']
                
    classif.append(class_img)
    clouds.append(cloud)
    reg.append(reg_vis)
    regX.append(reg_x)
    regY.append(reg_y)
    prom.append(prom_vis)
    promX.append(solar_prom_x)
    promY.append(solar_prom_y)
    promX1.append(solar_prom_x1)
    promY1.append(solar_prom_y1)
    promX2.append(solar_prom_x2)
    promY2.append(solar_prom_y2)
    promX3.append(solar_prom_x3)
    promY3.append(solar_prom_y3)
    promX4.append(solar_prom_x4)
    promY4.append(solar_prom_y4)
        

classif = []
clouds = []
reg = []
regX = []
regY = []
prom = []
promX = []
promY = []
promX1 = []
promY1 = []
promX2 = []
promY2 = []
promX3 = []
promY3 = []
promX4 = []
promY4 = []
idLst = []
storage = []

responses = list(data['annotations'][349:])
for i in range(len(responses)):
    idLst.append(json.loads(data['subject_data'][i])[str(data['subject_ids'][i])]['id'])
    storage.append(json.loads(data['subject_data'][i])[str(data['subject_ids'][i])]['storage_uri'])
    annotation = json.loads(responses[i])
    decode(annotation)

assert len(clouds) == len(classif) == len(reg) == len(regX) == len(regY) == len(prom) == len(promX) == len(promY) == len(responses)

df = pd.DataFrame({'id': idLst, 'reg_visible': reg, 'reg_x':regX, 'reg_y': regY, 'clouds': clouds, 'prominences': prom, 'prominences_x': promX, 'prominences_y': promY, 'prominences_x1': promX1, 'prominences_y1': promY1, 'prominences_x2': promX2, 'prominences_y2': promY2, 'prominences_x3': promX3, 'prominences_y3': promY3, 'prominences_x4': promX4, 'prominences_y4': promY4, 'image_classif': classif, 'storage': storage})
df = df.reindex_axis(['id','storage','image_classif','reg_visible', 'reg_x','reg_y','prominences','prominences_x','prominences_y', 'prominences_x1','prominences_y1', 'prominences_x2','prominences_y2', 'prominences_x3','prominences_y3', 'prominences_x4','prominences_y4', 'clouds'], axis=1)
df.to_csv('megamovie_classifications.csv', encoding='utf-8', sep=',')
