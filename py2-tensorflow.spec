### RPM external py2-tensorflow 1.1.0
## INITENV +PATH PYTHONPATH %{i}/${PYTHON_LIB_SITE_PACKAGES}

Source: none

Requires: tensorflow-sources
Requires: python
BuildRequires: py2-pip
Requires: py2-funcsigs py2-protobuf py2-pbr py2-six py2-packaging py2-appdirs py2-setuptools py2-pyparsing py2-numpy py2-mock

%prep

%build

#presumably this will be architecture dependent.
%define tensor_build cp27-cp27mu-linux_x86_64

mkdir -p %{i}
export PYTHONUSERBASE=%i
pip list
pip install --user -v ${TENSORFLOW_SOURCES_ROOT}/tensorflow-%{realversion}-%{tensor_build}.whl

%install

perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/tensorboard
