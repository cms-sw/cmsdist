### RPM external py2-prompt_toolkit 1.0.15
## INITENV +PATH PYTHON27PATH %{i}/${PYTHON_LIB_SITE_PACKAGES}
## INITENV +PATH PYTHON3PATH %{i}/${PYTHON3_LIB_SITE_PACKAGES}


%define pip_name prompt_toolkit
Requires: py2-six py2-wcwidth 

## IMPORT build-with-pip

