### RPM external py2-cryptography 2.4.2
## IMPORT build-with-pip

Requires: openssl py2-cffi py2-asn1crypto py2-enum34 py2-idna py2-ipaddress py2-six
%define PipPreBuild export LDFLAGS="-L${OPENSSL_ROOT}/lib"; \
                    export CFLAGS="-I${OPENSSL_ROOT}/include"
