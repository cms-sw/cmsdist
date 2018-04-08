### RPM external py2-traitlets 4.3.2
## INITENV +PATH PYTHON27PATH %{i}/${PYTHON_LIB_SITE_PACKAGES}
## INITENV +PATH PYTHON3PATH %{i}/${PYTHON3_LIB_SITE_PACKAGES}


%define pip_name traitlets
Requires: py2-ipython_genutils py2-six py2-decorator 

## IMPORT build-with-pip

