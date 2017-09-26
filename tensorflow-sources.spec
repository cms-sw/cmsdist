### RPM external tensorflow-sources 1.3.0
#Source: https://github.com/tensorflow/tensorflow/archive/v%{realversion}.tar.gz
%define tag 9e76bf324f6bac63137a02bb6e6ec9120703ea9b
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
incDir="tensorflow_cc/include"
libDir="tensorflow_cc/lib"

# Make directory and clean it
mkdir -p $incDir
mkdir -p $libDir

rm -rf $incDir/*
rm -rf $libDir/*

#Download depencies used by tensorflow and copy to include dir
tensorflow/contrib/makefile/download_dependencies.sh
cp -a tensorflow/contrib/makefile/downloads/* $incDir

# Copy .h & .cc files
cp -a bazel-genfiles/. 				$incDir
cp -a tensorflow/cc 					$incDir/tensorflow
cp -a tensorflow/core 				$incDir/tensorflow
cp -a third_party					$incDir


%install
#export PYTHONPATH=%{i}/lib/python:${PYTHONPATH}
#export PYTHONPATH=%{i}/${PYTHON_LIB_SITE_PACKAGES}:${PYTHONPATH}
bazel-bin/tensorflow/tools/pip_package/build_pip_package %{i}

#it looks like this tensorflow build pushes a number of third-party things to the bin area for now
#that needs to be cleaned up  
#perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/*

cp $PWD/bazel-bin/tensorflow/tools/lib_package/libtensorflow.tar.gz %{i}

#tar xfz $PWD/bazel-bin/tensorflow/tools/lib_package/libtensorflow.tar.gz -C %{i}

tar cfz %{i}/libtensorflow_cc.tar.gz tensorflow_cc/*
