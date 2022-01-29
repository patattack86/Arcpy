import boto3
import arcpy
import os
from botocore.handlers import disable_signing

s3 = boto3.resource('s3')
s3.meta.client.meta.events.register('choose-signer.s3.*', disable_signing)

bucket = s3.Bucket('njogis-imagery')

my_bucket = s3.Bucket(bucket)

mosaic_dataset = r"B:\Woolpert\ArcProPython\Tutorial_geodatabse.gdb\youtube_dataset"

prefix = "2015/cog"

counter = 0
images_to_add = []

for file in my_bucket.objects.filter(Prefix=prefix):
    counter += 1
    vsis3_image_path = os.path.join("/vsis3/", bucket, file.key). replace('\\','/')
    print("Adding {}". format(vsis3_image_path))
    print("counter = {}". format(counter))

    images_to_add.append(vsis3_image_path)

    if counter > 25:
        break

arcpy.AddRastersToMosaicDataset_management(mosaic_dataset, "Raster Dataset", images_to_add)
print(arcpy.GetMessages())
print("Program Finished")
