### RPM external py2-pyparsing 2.0.3
## INITENV +PATH PYTHONPATH %{i}/$PYTHON_LIB_SITE_PACKAGES
%define my_name %(echo %n | cut -f2 -d-)
Source: http://downloads.sourceforge.net/project/%{my_name}/%{my_name}/%{my_name}-%{realversion}/%{my_name}-%{realversion}.zip
Requires: python
BuildRequires: py2-setuptools

%prep
%setup -n %{my_name}-%{realversion}

%build
python setup.py build

%install
python -c 'import setuptools; print(setuptools.__file__)'
python setup.py install --skip-build --prefix=%{i}
find %{i}/${PYTHON_LIB_SITE_PACKAGES} -name '*.egg-info' -type d -print0 | xargs -0 rm -rf
