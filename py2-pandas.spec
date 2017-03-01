### RPM external py2-pandas 0.19.1
## INITENV +PATH PYTHONPATH %i/$PYTHON_LIB_SITE_PACKAGES
Source: https://pypi.python.org/packages/0b/9c/20a36af2016a9554378ebad2c69f63fd87bd0cc612eeed068fab656ec661/pandas-0.19.1.tar.gz
Patch0: py2-pandas-0.16.0
Requires: python
Requires: py2-numpy
Requires: py2-python-dateutil
Requires: py2-pytz
%prep
%setup -n pandas-%{realversion}
%patch0 -p1

%build
%install

mkdir -p %{i}/$PYTHON_LIB_SITE_PACKAGES
export PYTHONPATH=%{i}/$PYTHON_LIB_SITE_PACKAGES:${PYTHONPATH}

python setup.py build
python setup.py install --prefix=%{i}
find %{i} -name '*.egg-info' -exec rm {} \;
