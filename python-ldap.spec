### RPM external python-ldap 2.4.10
## INITENV +PATH PYTHON27PATH %{i}/${PYTHON_LIB_SITE_PACKAGES}

Requires: python openssl openldap

%define PipBuildOptions --global-option=build_ext --global-option="-L${OPENSSL_ROOT}/lib" --global-option="-L${PYTHON_ROOT}/lib" --global-option="-L${OPENLDAP_ROOT}/lib"  --global-option="-I${OPENSSL_ROOT}/include" --global-option="-I${PYTHON_ROOT}/include" --global-option="-I${OPENLDAP_ROOT}/include"  --global-option="-UHAVE_SASL"

%define pip_name python-ldap


## IMPORT build-with-pip

