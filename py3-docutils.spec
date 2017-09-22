### RPM external py3-docutils 0.12
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}

Source0: svn://docutils.svn.sourceforge.net/svnroot/docutils/trunk/sandbox/rst2wiki@7467?scheme=https&strategy=export&module=sandbox&output=/rst2wiki.tar.gz
Source1: http://downloads.sourceforge.net/docutils/docutils-%{realversion}.tar.gz
Requires: python3

%prep
%setup -T -b 0 -n sandbox
%setup -D -T -b 1 -n docutils-%realversion

%build
python3 setup.py build

%install
python3 setup.py install --prefix=%i
cp ../sandbox/tools/rst2wiki.py %i/bin/
cp ../sandbox/docutils/writers/wiki.py %i/$PYTHON_LIB_SITE_PACKAGES/docutils/writers/
python3 -m compileall %i/$PYTHON_LIB_SITE_PACKAGES

# replace all instances of #!/path/bin/python into proper format
%py3PathRelocation

# Generate dependencies-setup.{sh,csh} so init.{sh,csh} picks full environment.
%addDependency

%post
%{relocateConfig}etc/profile.d/dependencies-setup.*sh
