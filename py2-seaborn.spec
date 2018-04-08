### RPM external py2-seaborn 0.8.1
## INITENV +PATH PYTHON27PATH %{i}/${PYTHON_LIB_SITE_PACKAGES}
## INITENV +PATH PYTHON3PATH %{i}/${PYTHON3_LIB_SITE_PACKAGES}

Requires: py2-matplotlib py2-numpy py2-scipy py2-pandas

%define pip_name seaborn


## IMPORT build-with-pip

