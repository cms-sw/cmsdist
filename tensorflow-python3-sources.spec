### RPM external tensorflow-python3-sources 1.12.0
#Source: https://github.com/tensorflow/tensorflow/archive/v%{realversion}.tar.gz
# NOTE: whenever the version of tensorflow changes, update it also in tensorflow-c tensorflow-cc and py2-tensorflow
%define isslc6amd64 %(case %{cmsplatf} in (slc6_amd64_*) echo 1 ;; (*) echo 0 ;; esac)
%define tag 9150f29bf90ec79e01c707f2820409b9e05c6f73
%define branch cms/v%{realversion}
%define github_user cms-externals
Source: git+https://github.com/%{github_user}/tensorflow.git?obj=%{branch}/%{tag}&export=tensorflow-%{realversion}&output=/tensorflow-%{realversion}-%{tag}.tgz

BuildRequires: bazel
Requires: gcc protobuf java-env python3 py2-numpy py2-enum34 py2-mock py2-wheel py2-Keras-Applications py2-Keras-Preprocessing py2-setuptools

%prep

%setup -q -n tensorflow-%{realversion}

%build

export PYTHON_BIN_PATH=`which python3`
export TF_NEED_JEMALLOC=0
export TF_NEED_HDFS=0
export CC_OPT_FLAGS=-march=core2
export CXX_OPT_FLAGS=-std=c++11
export TF_NEED_GCP=0
export TF_ENABLE_XLA=0
export TF_NEED_OPENCL=0
export TF_NEED_CUDA=0
export TF_NEED_VERBS=0
export TF_NEED_MKL=0
export TF_NEED_MPI=0
export USE_DEFAULT_PYTHON_LIB_PATH=1
export TF_NEED_S3=0
export TF_NEED_GDR=0
export TF_NEED_OPENCL_SYCL=0
export TF_SET_ANDROID_WORKSPACE=false
export TF_NEED_KAFKA=false
export TF_NEED_AWS=0
export TF_DOWNLOAD_CLANG=0
export TF_NEED_IGNITE=false
export TF_NEED_ROCM=false

#and source locations
#export EIGEN_SOURCE=${EIGEN_SOURCE} # we are using tf own eigen now
export PROTOBUF_SOURCE=${PROTOBUF_SOURCE}
#export ZLIB_SOURCE=${ZLIB_SOURCE}
export LIBJPEG_TURBO_SOURCE="https://github.com/libjpeg-turbo/libjpeg-turbo/archive/2.0.1.tar.gz"

#${LIBJPEG_TURBO_SOURCE}

#export EIGEN_STRIP_PREFIX=${EIGEN_STRIP_PREFIX} # we are using tf own eigen now
export PROTOBUF_STRIP_PREFIX=${PROTOBUF_STRIP_PREFIX}
#export ZLIB_STRIP_PREFIX= ${ZLIB_STRIP_PREFIX}
export LIBJPEG_TURBO_STRIP_PREFIX="libjpeg-turbo-2.0.1"

#temp directory
rm -rf ../build

./configure

BAZEL_OPTS="--output_user_root ../build build -s --verbose_failures -c opt --cxxopt=${CXX_OPT_FLAGS}"
BAZEL_EXTRA_OPTS="--action_env PYTHONPATH=${PYTHON3PATH} --distinct_host_configuration=false"

bazel $BAZEL_OPTS $BAZEL_EXTRA_OPTS //tensorflow/tools/pip_package:build_pip_package
bazel $BAZEL_OPTS $BAZEL_EXTRA_OPTS //tensorflow:libtensorflow_cc.so
bazel $BAZEL_OPTS $BAZEL_EXTRA_OPTS //tensorflow/tools/lib_package:libtensorflow
bazel $BAZEL_OPTS $BAZEL_EXTRA_OPTS //tensorflow/python/tools:tools_pip
bazel $BAZEL_OPTS $BAZEL_EXTRA_OPTS //tensorflow/tools/graph_transforms:transform_graph

bazel shutdown

#Copying out what was built by bazel
incdir="$PWD/tensorflow_cc/include"
libdir="$PWD/tensorflow_cc/lib"
bindir="$PWD/tensorflow_cc/bin"

# Make directory and clean it
rm -rf $incdir $libdir $bindir
mkdir -p $incdir $libdir $bindir

cp -v $PWD/bazel-bin/tensorflow/libtensorflow_cc.so $libdir
cp -v $PWD/bazel-bin/tensorflow/libtensorflow_framework.so $libdir

#Download depencies used by tensorflow and copy to include dir
tensorflow/contrib/makefile/download_dependencies.sh
tdir=$PWD
dwnldir=$PWD/tensorflow/contrib/makefile/downloads
gendir=$PWD/bazel-genfiles

# tensorflow headers
cd ${tdir}
header_list=`find tensorflow -type f -name "*.h" | grep -v contrib`
for my_header in ${header_list}
do
  my_header_dir=$(dirname "${my_header}")
  mkdir -p ${incdir}/${my_header_dir}
  cp -p ${my_header} ${incdir}/${my_header_dir}
done
# generated headers
cd ${gendir}
header_list=`find tensorflow -type f -name "*.h"`
for my_header in ${header_list}
do
  my_header_dir=$(dirname "${my_header}")
  mkdir -p ${incdir}/${my_header_dir}
  cp -p ${my_header} ${incdir}/${my_header_dir}
done
# third party headers
cd ${tdir}
header_list=`find third_party -type f -name "*.h" | grep -v contrib`
for my_header in ${header_list}
do
  my_header_dir=$(dirname "${my_header}")
  mkdir -p ${incdir}/${my_header_dir}
  cp -p ${my_header} ${incdir}/${my_header_dir}
done
# third party eigen headers
header_list=`find third_party/eigen3 -type f | grep -v contrib`
for my_header in ${header_list}
do
  my_header_dir=$(dirname "${my_header}")
  mkdir -p ${incdir}/${my_header_dir}
  cp -p ${my_header} ${incdir}/${my_header_dir}
done
# downloaded headers
cd ${dwnldir}
header_list=`find gemmlowp googletest re2 -type f -name "*.h"`
for my_header in ${header_list}
do
  my_header_dir=$(dirname "${my_header}")
  mkdir -p ${incdir}/${my_header_dir}
  cp -p ${my_header} ${incdir}/${my_header_dir}
done
# downloaded eigen headers
header_list=`find eigen/Eigen eigen/unsupported -type f`
for my_header in ${header_list}
do
  my_header_dir=$(dirname "${my_header}")
  mkdir -p ${incdir}/${my_header_dir}
  cp -p ${my_header} ${incdir}/${my_header_dir}
done
# downloaded nsync headers
header_list=`find nsync/public -name '*.h' -type f`
for my_header in ${header_list}
do
  cp -p ${my_header} ${incdir}/
done
# eigen signature file
cp -p eigen/signature_of_eigen3_matrix_library ${incdir}/eigen/ || exit 1

%install

bazel-bin/tensorflow/tools/pip_package/build_pip_package %{i}

cp $PWD/bazel-bin/tensorflow/tools/lib_package/libtensorflow.tar.gz %{i}
cd tensorflow_cc
tar cfz %{i}/libtensorflow_cc.tar.gz .
