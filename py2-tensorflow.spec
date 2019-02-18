### RPM external py2-tensorflow 1.13.0rc2
## INITENV +PATH PYTHON27PATH %{i}/${PYTHON_LIB_SITE_PACKAGES}
## INITENV +PATH PYTHON3PATH %{i}/${PYTHON3_LIB_SITE_PACKAGES}

Source: none

BuildRequires: tensorflow-sources tensorflow-python3-sources py2-pip
Requires: python python3 py2-funcsigs py2-protobuf py2-pbr py2-six py2-packaging py2-appdirs py2-setuptools py2-pyparsing py2-numpy py2-mock py2-Werkzeug py2-enum34 py2-keras-applications py2-keras-preprocessing libjpeg-turbo eigen protobuf nasm py2-wheel

%prep

%build

%ifarch x86_64
%define tensor_build cp27-cp27mu-linux_x86_64
%define tensor_python3_build cp36-cp36m-linux_x86_64
%endif
%ifarch aarch64
%define tensor_build cp27-cp27mu-linux_aarch64
%define tensor_python3_build cp36-cp36m-linux_aarch64
%endif

mkdir -p %{i}
export PYTHONUSERBASE=%i
pip list
pip install --user -v ${TENSORFLOW_SOURCES_ROOT}/tensorflow-%{realversion}-%{tensor_build}.whl
pip3 list
pip3 install --user -v ${TENSORFLOW_PYTHON3_SOURCES_ROOT}/tensorflow-%{realversion}-%{tensor_python3_build}.whl

%install
perl -p -i -e "s|^#!.*python(.*)|#!/usr/bin/env python$1|" %{i}/bin/*

