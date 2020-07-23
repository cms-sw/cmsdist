### RPM external cupla 0.2.0

Source: https://github.com/alpaka-group/%{n}/archive/%{realversion}.tar.gz
Requires: alpaka
Requires: cuda
Requires: tbb

%prep
%setup -n %{n}-%{realversion}

%build
## INCLUDE cuda-flags
# defines nvcc_cuda_flags and nvcc_stdcxx

mkdir build lib

# remove the version of Alpaka bundled with Cupla
rm -rf alpaka

CXXFLAGS="-DALPAKA_DEBUG=0 -I$CUDA_ROOT/include -I$TBB_ROOT/include -I$BOOST_ROOT/include -I$ALPAKA_ROOT/include -Iinclude"
HOST_FLAGS="%{nvcc_stdcxx} -O2 -pthread -fPIC -Wall -Wextra"
NVCC_FLAGS="%{nvcc_cuda_flags}"
FILES=$(find src -type f -name *.cpp)

# build the serial CPU backend
mkdir build/serial
for FILE in $FILES; do
  g++ -DALPAKA_ACC_CPU_B_SEQ_T_SEQ_ENABLED -DCUPLA_STREAM_ASYNC_ENABLED=0 $CXXFLAGS $HOST_FLAGS -c $FILE -o build/serial/$(basename $FILE).o
done
g++ $CXXFLAGS $HOST_FLAGS build/serial/*.o -shared -o lib/libcupla-serial.so

# build the TBB CPU backend
mkdir build/tbb
for FILE in $FILES; do
  g++ -DALPAKA_ACC_CPU_B_TBB_T_SEQ_ENABLED -DCUPLA_STREAM_ASYNC_ENABLED=1 $CXXFLAGS $HOST_FLAGS -c $FILE -o build/tbb/$(basename $FILE).o
done
g++ $CXXFLAGS $HOST_FLAGS build/tbb/*.o -L$TBB_ROOT/lib -ltbb -shared -o lib/libcupla-tbb.so

# build the CUDA GPU backend
if [ $(%{cuda_gcc_support}) = true ] ; then
  mkdir build/cuda
  for FILE in $FILES; do
    $CUDA_ROOT/bin/nvcc -DALPAKA_ACC_GPU_CUDA_ENABLED -DCUPLA_STREAM_ASYNC_ENABLED=1 $CXXFLAGS $NVCC_FLAGS -Xcompiler "$HOST_FLAGS" -x cu -c $FILE -o build/cuda/$(basename $FILE).o
  done
  g++ $CXXFLAGS $HOST_FLAGS build/cuda/*.o -L$CUDA_ROOT/lib64 -lcudart -shared -o lib/libcupla-cuda.so
fi

%install
cp -ar include %{i}/include
cp -ar lib %{i}/lib

%post
