1. [Installation](https://github.com/roboticslab-uc 3m/installation-guides/blob/master/install-openn i-nite.md)  
2. pip install primesense 
3. from primesense import openni2
4. [install](https://naman5.wordpress.com/2014/06/24/experimenting-with-kinect-using-opencv-python-and-open-kinect-libfreenect/)

> <code> 
  openni2.initialize("/home/aghinsa/repos/OpenNI2/Bin/x64-Release")  
  dev = openni2.Device.open_any()  
  print dev.get_sensor_info()  
  depth_stream = dev.create_depth_stream()  
  depth_stream.start()  
  frame = depth_stream.read_frame()  
  frame_data = frame.get_buffer_as_uint16()  
  depth_stream.stop()  
  openni2.unload()  
</code>
