### RPM external py3-cryptography 2.4.2
## IMPORT build-with-pip3

Requires: openssl py3-cffi py3-asn1crypto py3-enum34 py3-idna py3-ipaddress py3-six
%define PipPreBuild export LDFLAGS="-L${OPENSSL_ROOT}/lib"; \
                    export CFLAGS="-I${OPENSSL_ROOT}/include"
