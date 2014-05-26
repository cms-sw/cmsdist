### RPM external py2-sqlalchemy 0.5.2
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}

Source: http://downloads.sourceforge.net/sqlalchemy/SQLAlchemy-%realversion.tar.gz
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
