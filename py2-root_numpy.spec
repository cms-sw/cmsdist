### RPM external py2-root_numpy 4.6.0
## INITENV +PATH PYTHONPATH %{i}/$PYTHON_LIB_SITE_PACKAGES
%define my_name %(echo %n | cut -f2 -d-)
Source: https://github.com/rootpy/%my_name/archive/%{realversion}.tar.gz

Requires: python py2-numpy root
BuildRequires: py2-setuptools

%prep
%setup -n %{my_name}-%{realversion}

%build
python setup.py build

%install
python setup.py install --single-version-externally-managed --record=/dev/null --skip-build --prefix=%{i}
find %{i}/${PYTHON_LIB_SITE_PACKAGES} -name '*.egg-info' -print0 | xargs -0 rm -rf
