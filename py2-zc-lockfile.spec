### RPM external py2-zc-lockfile 1.4
## IMPORT build-with-pip
%define pip_name zc.lockfile

%define PipPostBuild touch %i/${PYTHON_LIB_SITE_PACKAGES}/zc/__init__.py
