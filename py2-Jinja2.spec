### RPM external py2-Jinja2 2.10
## INITENV +PATH PYTHON27PATH %{i}/${PYTHON_LIB_SITE_PACKAGES}
## INITENV +PATH PYTHON3PATH %{i}/${PYTHON3_LIB_SITE_PACKAGES}


%define pip_name Jinja2
Requires: py2-MarkupSafe 

## IMPORT build-with-pip

