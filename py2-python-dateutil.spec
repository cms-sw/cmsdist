### RPM external py2-python-dateutil 1.5
## INITENV +PATH PYTHONPATH %{i}/$PYTHON_LIB_SITE_PACKAGES

Source: http://labix.org/download/python-dateutil/python-dateutil-%{realversion}.tar.gz
Requires: python
Requires: py2-setuptools

%prep
%setup -n python-dateutil-%{realversion} 

%build
python setup.py build

%install
mkdir -p %{i}/$PYTHON_LIB_SITE_PACKAGES
export PYTHONPATH=%{i}/$PYTHON_LIB_SITE_PACKAGES:${PYTHONPATH}
python setup.py install --prefix=%{i}
find %{i} -name '*.egg-info' -exec rm {} \;
