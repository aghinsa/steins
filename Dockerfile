FROM ubuntu:16.04




# Install apt-getable dependencies
RUN apt-get update \
    && apt-get install -y \
        build-essential \
        cmake \
        git \
        libatlas-base-dev \
        libboost-python-dev \
        libeigen3-dev \
        libgoogle-glog-dev \
        libopencv-dev \
        libsuitesparse-dev \
        python-dev \
        python-numpy \
        python-opencv \
        python-pip \
        python-pyexiv2 \
        python-pyproj \
        python-scipy \
        python-yaml \
        wget \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*





# Install opengv from source
RUN \
    mkdir -p /source && cd /source && \
    git clone https://github.com/paulinus/opengv.git && \
    cd /source/opengv && \
    mkdir -p build && cd build && \
    cmake .. -DBUILD_TESTS=OFF -DBUILD_PYTHON=ON && \
    make install && \
    cd / && \
    rm -rf /source/opengv


# Install python requirements
RUN \
    pip install exifread==2.1.2 \
                gpxpy==1.1.2 \
                networkx==1.11 \
                numpy \
                pyproj==1.9.5.1 \
                pytest==3.0.7 \
                python-dateutil==2.6.0 \
                PyYAML==3.12 \
                scipy \
                xmltodict==0.10.2 \
                cloudpickle==0.4.0 \
                loky==1.2.1
#INSTALL wormhole
RUN \
  pip install magic-wormhole



#openMVS
RUN \
apt-get update -qq &&  apt-get install -qq && \
apt-get -y install build-essential git mercurial cmake libpng-dev libjpeg-dev libtiff-dev libglu1-mesa-dev libxmu-dev libxi-dev && \
mkdir ~/building && \
cd ~/building && \
hg clone https://bitbucket.org/eigen/eigen#3.2 && \
mkdir eigen_build && cd eigen_build && \
cmake . ../eigen && \
make &&  make install && \
cd ~/building && \
apt-get -y install libboost-iostreams-dev libboost-program-options-dev libboost-system-dev libboost-serialization-dev && \
apt-get -y install libopencv-dev && \
apt-get -y install libcgal-dev libcgal-qt5-dev && \
git clone https://github.com/cdcseacave/VCG.git vcglib && \
apt-get -y install libatlas-base-dev libsuitesparse-dev && \
git clone https://ceres-solver.googlesource.com/ceres-solver ceres-solver && \
mkdir ceres_build && cd ceres_build && \
cmake . ../ceres-solver/ -DMINIGLOG=ON -DBUILD_TESTING=OFF -DBUILD_EXAMPLES=OFF && \
make -j2 && make install && \
cd ~/building && \
apt-get -y install freeglut3-dev libglew-dev libglfw3-dev && \
git clone https://github.com/cdcseacave/openMVS.git openMVS && \
mkdir openMVS_build && cd openMVS_build && \
cmake . ../openMVS -DCMAKE_BUILD_TYPE=Release -DVCG_ROOT="~/building/vcglib" && \
make -j2 &&  make install

# Install Ceres from source
RUN \
    mkdir -p /source && cd /source && \
    wget http://ceres-solver.org/ceres-solver-1.14.0.tar.gz && \
    tar xvzf ceres-solver-1.14.0.tar.gz && \
    cd /source/ceres-solver-1.14.0 && \
    mkdir -p build && cd build && \
    cmake .. -DCMAKE_C_FLAGS=-fPIC -DCMAKE_CXX_FLAGS=-fPIC -DBUILD_EXAMPLES=OFF -DBUILD_TESTING=OFF && \
    make install && \
    cd / && \
    rm -rf /source/ceres-solver-1.14.0 && \
    rm -f /source/ceres-solver-1.14.0.tar.gz

#opensfm
RUN \
    cd ~ && \
    git clone https://github.com/mapillary/OpenSfM.git && \
    cd OpenSfM && \
    pip install -r requirements.txt && \
    python setup.py build



RUN rm -rf ~/building
RUN echo "export PATH=$PATH:/usr/local/bin/OpenMVS" >> ~/.bashrc
