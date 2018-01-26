### RPM external tensorflow-sources 1.3.0
#Source: https://github.com/tensorflow/tensorflow/archive/v%{realversion}.tar.gz
%define tag 6438b7f7459232044dbb4e042f2c42cbdf925fad
%define branch cms/v%{realversion}
%define github_user cms-externals
Source: git+https://github.com/%{github_user}/tensorflow.git?obj=%{branch}/%{tag}&export=tensorflow-%{realversion}&output=/tensorflow-%{realversion}.tgz
Patch0: tensorflow-workspace

BuildRequires: bazel eigen protobuf gcc
Requires: py2-numpy python py2-wheel

%prep

%setup -q -n tensorflow-%{realversion}
%patch0 -p1

%build
export PYTHON_BIN_PATH=`which python`
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

#temp directory
rm -rf $PWD/dud

./configure

bazel --output_user_root $PWD/dud clean

bazel --output_user_root $PWD/dud fetch "tensorflow:libtensorflow_cc.so"
sed -i -e 's|mnemonic="ProtoCompile",|mnemonic="ProtoCompile", env=ctx.configuration.default_shell_env, |' `find $PWD/dud -name protobuf.bzl`

bazel --output_user_root $PWD/dud build -s --verbose_failures -c opt --cxxopt=$CXX_OPT_FLAGS tensorflow:libtensorflow_cc.so
#This is needed on SLC6 because the version of glibc is old
sed -i -e 's|"-lpthread", "-lm"|"-lpthread", "-lm", "-lrt"|' $PWD/dud/*/external/protobuf/BUILD
bazel --output_user_root $PWD/dud build -s --verbose_failures -c opt --cxxopt=$CXX_OPT_FLAGS //tensorflow/tools/pip_package:build_pip_package
bazel --output_user_root $PWD/dud build -s --verbose_failures -c opt --cxxopt=$CXX_OPT_FLAGS //tensorflow/tools/lib_package:libtensorflow

bazel shutdown


#Copying out what was built by bazel
incdir="$PWD/tensorflow_cc/include"
libdir="$PWD/tensorflow_cc/lib"

# Make directory and clean it
mkdir -p $incdir
mkdir -p $libdir

rm -rf $incdir/*
rm -rf $libdir/*

cp -v $PWD/bazel-bin/tensorflow/libtensorflow_cc.so $libdir

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
# eigen signature file
cp -p eigen/signature_of_eigen3_matrix_library ${incdir}/eigen/ || exit 1

%install
#export PYTHONPATH=%{i}/lib/python:${PYTHONPATH}
#export PYTHONPATH=%{i}/${PYTHON_LIB_SITE_PACKAGES}:${PYTHONPATH}
bazel-bin/tensorflow/tools/pip_package/build_pip_package %{i}

#it looks like this tensorflow build pushes a number of third-party things to the bin area for now
#that needs to be cleaned up  
#perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/*

cp $PWD/bazel-bin/tensorflow/tools/lib_package/libtensorflow.tar.gz %{i}

#tar xfz $PWD/bazel-bin/tensorflow/tools/lib_package/libtensorflow.tar.gz -C %{i}

tar cfz %{i}/libtensorflow_cc.tar.gz tensorflow_cc/.
