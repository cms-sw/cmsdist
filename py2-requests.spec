### RPM external py2-requests 2.5.1
## INITENV +PATH PYTHONPATH %{i}/$PYTHON_LIB_SITE_PACKAGES
%define my_name %(echo %n | cut -f2 -d-)
Source: https://github.com/kennethreitz/%my_name/archive/v%{realversion}.tar.gz
Requires: python
BuildRequires: py2-setuptools

%prep
%setup -n %{my_name}-%{realversion}

%build
python setup.py build

%install
python -c 'import setuptools; print(setuptools.__file__)'
python setup.py install --single-version-externally-managed --record=/dev/null --skip-build --prefix=%{i}
find %{i}/${PYTHON_LIB_SITE_PACKAGES} -name '*.egg-info' -type d -print0 | xargs -0 rm -rf
