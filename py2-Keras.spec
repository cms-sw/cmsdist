### RPM external py2-Keras 1.2.2
## INITENV +PATH PYTHONPATH %{i}/$PYTHON_LIB_SITE_PACKAGES


%define pip_name Keras
Requires: py2-PyYAML py2-six py2-scipy py2-Theano py2-numpy
## IMPORT build-with-pip


%define PipPostBuild \
   perl -p -i -e "s|# Default backend: TensorFlow.|# Default backend: Theano.|" %{i}/lib/python2.7/site-packages/keras/backend/__init__.py; \
   perl -p -i -e "s|_BACKEND = 'tensorflow'|_BACKEND = 'theano'|" %{i}/lib/python2.7/site-packages/keras/backend/__init__.py

