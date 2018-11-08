### RPM external py2-onnx 1.3.0
## IMPORT build-with-pip

Requires: cmake py2-numpy protobuf py2-protobuf py2-six py2-typing_extensions
%define PipPreBuild export ONNX_ML=1
%define PipPostBuild perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/*
