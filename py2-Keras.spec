### RPM external py2-Keras 1.2.2
## INITENV +PATH PYTHONPATH %{i}/$PYTHON_LIB_SITE_PACKAGES


%define pip_name Keras
Requires: py2-PyYAML py2-six py2-scipy py2-Theano py2-numpy
## IMPORT build-with-pip

