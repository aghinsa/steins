import subprocess
import argparse
import os
import time

parser=argparse.ArgumentParser()
parser.add_argument("-i","--input")
args=parser.parse_args()
image_dir=args.input

dirs=args.input.split('/')
dirs.pop()
dirs[0]=os.path.expanduser(dirs[0])
parent_dir='/'.join(dirs)

try:
    os.mkdir(os.path.join(parent_dir,"matches"))
except:
    pass

try:
    os.mkdir(os.path.join(parent_dir,"out"))
except:
    pass

matches_dir=os.path.join(parent_dir,'matches')
output_dir=os.path.join(parent_dir,'out')
camera_dir=os.path.join(parent_dir)
json=os.path.join(matches_dir,'sfm_data.json')

print('Starting reconstructing...')
tic=time.clock()

command="openMVG_main_SfMInit_ImageListing -i '{}' -d '{}' -o '{}' ".format(image_dir,camera_dir,matches_dir)
p=subprocess.Popen(command)
p.wait()

command="openMVG_main_ComputeFeatures -i '{}' -o '{}'".format(json,matches_dir)
p=subprocess.Popen(command)
p.wait()

command="openMVG_main_ComputeMatches -i '{}' -o '{}'".format(json,matches_dir)
p=subprocess.Popen(command)
p.wait()

command="openMVG_main_IncrementalSfM -i '{}' -m '{}' -o '{}'".format(json,matches_dir,output_dir)
p=subprocess.Popen(command)
p.wait()

bin=os.path.join(output_dir,'sfm_data.bin')
command="openMVG_main_openMVG2openMVS -i '{}' -o 'scene.mvs'".format(bin)
p=subprocess.Popen(command)
p.wait()

print('Starting mvs .......')

# DensifyPointCloud scene.mvs
# ReconstructMesh scene_dense.mvs
# RefineMesh scene_mesh.mvs
# TextureMesh scene_dense_mesh.mvs

command="DensifyPointCloud scene.mvs"
p=subprocess.Popen(command)
p.wait()
command="ReconstructMesh scene_dense.mvs"
p=subprocess.Popen(command)
p.wait()
command="TextureMesh scene_dense_mesh.mvs"
p=subprocess.Popen(command)
p.wait()

toc=time.clock()

print('Completed in {} minutes'.format((toc-tic)/60))

#mvg
