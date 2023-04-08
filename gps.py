import os 
directory = '/home/ranguy/main/manas/image_pipeline/test_delay'
for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    if os.path.isfile(f):
        name=filename.split('/')[-1]
        metadata_filename = name.split('_')[1:]
        metadata_filename[-1]=metadata_filename[-1].split('.')[0]
        try:
            print("- - "+metadata_filename[0]+"\n  - "+metadata_filename[1]+"\n  - "+metadata_filename[2])
        except:
            continue

