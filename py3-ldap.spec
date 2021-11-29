### RPM external py3-ldap 3.4.0
## IMPORT build-with-pip3

%define pip_name python-ldap

Requires: python3 openldap py3-pyasn1 py3-pyasn1modules

%define patchsrc0 sed -i -e "s|\\[_ldap\\]|[_ldap]\\ninclude_dirs = ${PYTHON3_ROOT}/include ${OPENLDAP_ROOT}/include|" setup.cfg
%define patchsrc1 sed -i -e "s|\\[_ldap\\]|[_ldap]\\nlibrary_dirs = ${PYTHON3_ROOT}/lib ${OPENLDAP_ROOT}/lib|" setup.cfg
%define patchsrc2 sed -i -e "s|HAVE_SASL||" setup.cfg
