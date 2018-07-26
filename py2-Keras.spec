### RPM external py2-Keras 2.2.0
## INITENV +PATH PYTHON27PATH %{i}/${PYTHON_LIB_SITE_PACKAGES}
## INITENV +PATH PYTHON3PATH %{i}/${PYTHON3_LIB_SITE_PACKAGES}

%define pip_name Keras
Requires: py2-PyYAML py2-six py2-scipy py2-Theano py2-numpy
## IMPORT build-with-pip


