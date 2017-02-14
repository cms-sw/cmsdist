### RPM external py2-tensorflow 0.12.1
## INITENV +PATH PYTHONPATH %{i}/$PYTHON_LIB_SITE_PACKAGES

# nothing on pypi is ok for tensorflow at this point
%define tensorflowSource https://storage.googleapis.com/tensorflow/linux/cpu/tensorflow-0.12.1-cp27-none-linux_x86_64.whl
%define PipDownloadOptions ALTSRC%%20%tensorflowSource%%20--no-deps%%20--no-binary%%3D:none:
%define pip_name tensorflow
Requires: py2-funcsigs py2-protobuf py2-pbr py2-six py2-packaging py2-appdirs py2-setuptools py2-pyparsing py2-numpy py2-mock
## IMPORT build-with-pip

%define PipPostBuild \
  perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/tensorboard

