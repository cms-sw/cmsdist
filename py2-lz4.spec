### RPM external py2-lz4 1.1.0
## INITENV +PATH PYTHON27PATH %{i}/${PYTHON_LIB_SITE_PACKAGES}
## INITENV +PATH PYTHON3PATH %{i}/${PYTHON3_LIB_SITE_PACKAGES}

Requires: lz4

%define PipBuildOptions  --global-option=build_ext --global-option="-L${LZ4_ROOT}/lib"  --global-option="-I${LZ4_ROOT}/include"

## IMPORT build-with-pip

%define PipPostBuild perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/*
