### RPM external py3-pip 26.0.1
## INITENV +PATH PATH %{i}/bin
## INITENV +PATH LD_LIBRARY_PATH %{i}/lib
## INITENV +PATH PYTHON3PATH %{i}/${PYTHON3_LIB_SITE_PACKAGES}
%define my_name %(echo %n | cut -f2 -d-)
Source: https://raw.githubusercontent.com/pypa/get-pip/refs/tags/%{realversion}/public/get-pip.py
Requires: python3 py3-setuptools

%prep

%build
python3 %{_sourcedir}/get-pip.py  --no-setuptools --no-wheel pip==%{realversion} --prefix=%{i}

%install
%relocatePy3Shebang bin ${PYTHON3_LIB_SITE_PACKAGES}

