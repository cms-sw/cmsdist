### RPM external py2-pygithub 1.23.0
## INITENV +PATH PYTHON27PATH %{i}/${PYTHON_LIB_SITE_PACKAGES}
## INITENV +PATH PYTHON3PATH %{i}/${PYTHON3_LIB_SITE_PACKAGES}
Source: https://github.com/jacquev6/PyGithub/archive/v%{realversion}.zip
Requires: python
BuildRequires: py2-setuptools

%prep
%setup -n PyGithub-%{realversion}

%build
python setup.py build

%install
python -c 'import setuptools; print(setuptools.__file__)'
python setup.py install --single-version-externally-managed --record=/dev/null --skip-build --prefix=%{i}
find %{i}/${PYTHON_LIB_SITE_PACKAGES} -name '*.egg-info' -type d -print0 | xargs -0 rm -rf
# bla bla
