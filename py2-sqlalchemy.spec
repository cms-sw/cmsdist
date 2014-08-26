### RPM external py2-sqlalchemy 0.9.6
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}

Source: https://pypi.python.org/packages/source/S/SQLAlchemy/SQLAlchemy-%realversion.tar.gz
Requires: python 
# Apply patch to make ORACLE works correctly while specifying owner, see
# http://groups.google.com/group/sqlalchemy/browse_thread/thread/902d39df9bc8cf21
#Patch: py2-sqlalchemy_patch_0.4.4_0.4.5


%prep
%setup -n SQLAlchemy-%realversion

%build
python setup.py build

%install
python setup.py install --prefix=%i
find %i -name '*.egg-info' -exec rm {} \;
