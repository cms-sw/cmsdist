### RPM external py2-prompt_toolkit 1.0.14
## INITENV +PATH PYTHONPATH %{i}/${PYTHON_LIB_SITE_PACKAGES}


%define pip_name prompt_toolkit
Requires: py2-six py2-wcwidth 

## IMPORT build-with-pip

