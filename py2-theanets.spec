### RPM external py2-theanets 0.7.3
## INITENV +PATH PYTHON27PATH %{i}/${PYTHON_LIB_SITE_PACKAGES}

%define pip_name theanets
Requires: py2-numpy py2-Theano py2-downhill py2-climate

## IMPORT build-with-pip


