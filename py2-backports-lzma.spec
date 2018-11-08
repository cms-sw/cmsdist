### RPM external py2-backports-lzma 0.0.13
## IMPORT build-with-pip

%define doPython3 no
Requires: xz

%define pip_name backports.lzma

%define PipBuildOptions  --global-option=build_ext --global-option="-L${XZ_ROOT}/lib"  --global-option="-I${XZ_ROOT}/include"
