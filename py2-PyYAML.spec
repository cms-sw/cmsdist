### RPM external py2-PyYAML 3.11
## INITENV +PATH PYTHONPATH %{i}/$PYTHON_LIB_SITE_PACKAGES

%define my_name %(echo %n | cut -f2 -d-)
Source: http://pyyaml.org/download/pyyaml/%{my_name}-%{realversion}.tar.gz
Requires: python

%prep
%setup -n %{my_name}-%{realversion}

%build
python setup.py build

%install
python setup.py install --skip-build --prefix=%{i}
find %{i}/${PYTHON_LIB_SITE_PACKAGES} -name '*.egg-info' -type d -print0 | xargs -0 rm -rf
