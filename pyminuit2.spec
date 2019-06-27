### RPM external pyminuit2 0.0.1
## INITENV +PATH PYTHON27PATH %{i}/${PYTHON_LIB_SITE_PACKAGES}
Source: http://pyminuit2.googlecode.com/files/%{n}-%{realversion}.tar.gz
Requires: root 

Patch0: pyminuit2-cling

%prep
%setup -n %{n}-%{realversion}
%patch0 -p1

%build
%install
python setup.py install --prefix=%{i}
find %{i}/${PYTHON_LIB_SITE_PACKAGES} -name '*.egg-info' -print0 | xargs -0 rm -rf
# bla bla
