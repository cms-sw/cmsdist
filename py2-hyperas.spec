### RPM external py2-hyperas 0.4
## INITENV +PATH PYTHON27PATH %{i}/${PYTHON_LIB_SITE_PACKAGES}
## INITENV +PATH PYTHON3PATH %{i}/${PYTHON3_LIB_SITE_PACKAGES}

Requires: py2-Keras py2-hyperopt py2-entrypoints py2-jupyter py2-nbformat py2-nbconvert

%define pip_name hyperas


## IMPORT build-with-pip

