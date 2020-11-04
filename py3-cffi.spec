### RPM external py3-cffi 1.14.3
## IMPORT build-with-pip3

Requires: py3-pycparser libffi
%define PipBuildOptions --global-option=build_ext --global-option="-L${LIBFFI_ROOT}/lib64" --global-option="-I${LIBFFI_ROOT}/include"
