### RPM external py2-numexpr 2.6.8
## INITENV +PATH PYTHON27PATH %{i}/${PYTHON_LIB_SITE_PACKAGES}
## INITENV +PATH PYTHON3PATH %{i}/${PYTHON3_LIB_SITE_PACKAGES}

%define pip_name numexpr
Requires: py2-numpy 
Requires: python


## IMPORT build-with-pip

