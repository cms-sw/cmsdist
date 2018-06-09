### RPM external py2-lz4 1.1.0
## INITENV +PATH PYTHON27PATH %{i}/${PYTHON_LIB_SITE_PACKAGES}
## INITENV +PATH PYTHON3PATH %{i}/${PYTHON3_LIB_SITE_PACKAGES}

Requires: xz

%define PipBuildOptions  --global-option=build_ext --global-option="-L${XZ_ROOT}/lib"  --global-option="-I${XZ_ROOT}/include"

## IMPORT build-with-pip

