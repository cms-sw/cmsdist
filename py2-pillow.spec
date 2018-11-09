### RPM external py2-pillow 5.3.0
## IMPORT build-with-pip

Requires: libjpeg-turbo zlib
%define PipPreBuild export LDFLAGS="-L${LIBJPEG_TURBO_ROOT}/lib -L${ZLIB_ROOT}/lib"; \
                    export CFLAGS="-I${LIBJPEG_TURBO_ROOT}/include -I${ZLIB_ROOT}/include"
