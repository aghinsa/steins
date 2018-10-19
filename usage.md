1. [OpenMVG](#openmvg)
2. [OpenMVS](#openmvs)
3. [OpenCV Contrib](#opencv)
4. [SSH](#ssh)

### <a name="openmvg"></a> OpenMVG
* -d openMVG/src/openMVG/exif/sensor_width_database/sensor_width_camera_database.txt
* use the -f option on openMVG_main_SfMInit_ImageListing (-f std::max(w,h)*1.2), if no usable intrinsics  

> openMVG_main_SfMInit_ImageListing -i $imagedir$ -d $camera-params$ -o $matchesdir$  
  openMVG_main_ComputeFeatures -i ..\matches\sfm_data.json -o ...\matches  
  openMVG_main_ComputeMatches -i ..\matches\sfm_data.json -o ...\matches  
  openMVG_main_IncrementalSfM -i Dataset/matches/sfm_data.json -m Dataset/matches/ -o Dataset/out_Incremental_Reconstruction/ 
   
>  exporting to openmvs;run in outdir
>   openMVG_main_openMVG2openMVS -i sfm_data.bin -o scene.mvs
  

### <a name="openmvs"></a> OpenMVS
* export PATH=$PATH:/usr/local/bin/OpenMVS
> DensifyPointCloud scene.mvs  
ReconstructMesh scene_dense.mvs  
RefineMesh scene_mesh.mvs  
TextureMesh scene_dense_mesh.mvs  
TextureMesh.exe --resolution-level 3 scene_dense_mesh.mvs


### <a name="opencv"></a> OpenCV Contrib

* Download opencv and opencv contrib from git

<code> mkdir build  
cd build  
cmake -DCMAKE_BUILD_TYPE=RELEASE \  
	-DCMAKE_INSTALL_PREFIX=/usr/local \  
	-DINSTALL_PYTHON_EXAMPLES=ON \  
	-DINSTALL_C_EXAMPLES=OFF \  
	-DOPENCV_EXTRA_MODULES_PATH=~/opencv_contrib-3.4.1/modules \  
	-DPYTHON_EXECUTABLE=~/anaconda3/bin/python3 \  
	-DPYTHON_LIBRARY=~/anaconda3/lib/libpython3.6m.so \  
	-DPYTHON_NUMPY_INCLUDE_DIR=~/anaconda3/lib/python3.6/site-packages/numpy/core \  
	-DPYTHON_PACKAGES_PATH=~/anaconda3/lib/python3.6/site-packages \  
	-DBUILD_opencv_python3=yes \  
	-DBUILD_EXAMPLES=ON ..  
make -j4  
sudo make install  
cd /usr/local/lib/python3.6/site-packages/  
sudo mv cv2.cpython-36m-x86_64-linux-gnu.so cv2.so  
</code>

>sym link the installation to anaconda python  
ln -s /usr/local/lib/python3.6/site-packages/cv2.so cv2.so
