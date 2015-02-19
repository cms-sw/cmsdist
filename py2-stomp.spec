### RPM external py2-stomp 3.1.3
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}
Source: https://pypi.python.org/packages/source/s/stomp.py/stomp.py-%realversion.tar.gz
Requires: python 

%prep
%setup -n stomp.py-%realversion
#perl -p -i -e '/--static-libs/ && s/^(\s+)/$1"") #/' setup.py

%build
python setup.py build

%install
python setup.py install --prefix=%i
find %i -name '*.egg-info' -exec rm {} \;
# Remove documentation.
#%define drop_files %i/share
