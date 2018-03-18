### RPM external py2-scikit-learn 0.18.1
## INITENV +PATH PYTHON27PATH %{i}/${PYTHON_LIB_SITE_PACKAGES}

#%define PipPreBuild export ATLAS=None
%define pip_name scikit-learn
Requires: py2-numpy py2-scipy

## IMPORT build-with-pip
