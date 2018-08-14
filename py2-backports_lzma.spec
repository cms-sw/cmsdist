### RPM external py2-backports_lzma 0.0.13
## INITENV +PATH PYTHON27PATH %{i}/${PYTHON_LIB_SITE_PACKAGES}

%define doPython3 no
Requires: xz

%define pip_name backports.lzma

%define PipBuildOptions  --global-option=build_ext --global-option="-L${XZ_ROOT}/lib"  --global-option="-I${XZ_ROOT}/include"

## IMPORT build-with-pip

