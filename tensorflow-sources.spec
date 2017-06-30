### RPM external tensorflow-sources 1.2.1
Source: https://github.com/tensorflow/tensorflow/archive/v%{realversion}.tar.gz

BuildRequires: bazel
Requires: py2-numpy python py2-wheel

%prep

%setup -q -n tensorflow-%{realversion}

%build
export PYTHON_BIN_PATH=`which python`
export TF_NEED_JEMALLOC=0
export TF_NEED_HDFS=0
export CC_OPT_FLAGS="-march=native"
export TF_NEED_GCP=0
export TF_ENABLE_XLA=0
export TF_NEED_OPENCL=0
export TF_NEED_CUDA=0
export USE_DEFAULT_PYTHON_LIB_PATH=1

#temp directory
rm -rf $PWD/dud

sed -i -e 's|bazel clean|bazel --output_user_root $PWD/dud clean|' ./configure
sed -i -e 's|bazel fetch|bazel --output_user_root $PWD/dud fetch|' ./configure

./configure

sed -i -e 's|mnemonic="ProtoCompile",|mnemonic="ProtoCompile", env=ctx.configuration.default_shell_env, |' `find $PWD/dud -name protobuf.bzl`
sed -i -e 's|mnemonic="ProtoCompile",|mnemonic="ProtoCompile", use_default_shell_env=True,|' `find $PWD/dud -name protobuf.bzl`

bazel --output_user_root $PWD/dud build -s --verbose_failures --config=opt //tensorflow/tools/pip_package:build_pip_package
bazel --output_user_root $PWD/dud build -s --verbose_failures --config opt //tensorflow/tools/lib_package:libtensorflow

%install
#export PYTHONPATH=%{i}/lib/python:${PYTHONPATH}
#export PYTHONPATH=%{i}/${PYTHON_LIB_SITE_PACKAGES}:${PYTHONPATH}

bazel-bin/tensorflow/tools/pip_package/build_pip_package %{i}

#it looks like this tensorflow build pushes a number of third-party things to the bin area for now
#that needs to be cleaned up  
#perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/*

cp $PWD/bazel-bin/tensorflow/tools/lib_package/libtensorflow.tar.gz %{i}

#tar xfz $PWD/bazel-bin/tensorflow/tools/lib_package/libtensorflow.tar.gz -C %{i}




