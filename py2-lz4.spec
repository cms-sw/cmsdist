### RPM external py2-lz4 2.1.0
## IMPORT build-with-pip

Requires: lz4 py2-future

%define PipBuildOptions  --global-option=build_ext --global-option="-L${LZ4_ROOT}/lib"  --global-option="-I${LZ4_ROOT}/include"

%define PipPostBuild perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/*
