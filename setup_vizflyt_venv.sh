# load cuda 11.8 for nerfstudio
export CUDA_HOME=/usr/local/cuda-11.8
export PATH=$CUDA_HOME/bin:$PATH
export LD_LIBRARY_PATH=$CUDA_HOME/lib64:$LD_LIBRARY_PATH

# setup env
source $VIZFLYT_PATH/.vizflyt/bin/activate
cd $VIZFLYT_PATH/vizflyt_ws

# add the venv python interpreter to the setup.cfg in vizflyt
source $VIZFLYT_PATH/setup_cfg.sh

# build and source
colcon build
source install/setup.sh
source install/local_setup.sh

cd src