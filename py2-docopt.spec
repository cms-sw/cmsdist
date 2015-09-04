### RPM external py2-docopt 0.6.2
## INITENV +PATH PYTHONPATH %{i}/$PYTHON_LIB_SITE_PACKAGES

%define my_name %(echo %n | cut -f2 -d-)
Source: https://github.com/%{my_name}/%{my_name}/archive/%{realversion}.tar.gz
BuildRequires: py2-setuptools
Requires: python

%prep
%setup -n %{my_name}-%{realversion}

%build
python setup.py build

%install
python setup.py install --single-version-externally-managed --record=/dev/null --skip-build --prefix=%{i}
find %{i}/${PYTHON_LIB_SITE_PACKAGES} -name '*.egg-info' -type d -print0 | xargs -0 rm -rf
