### RPM external py3-scons 2.5.1
## INITENV +PATH PYTHONPATH %i/lib/%n-%realversion
Source: http://prdownloads.sourceforge.net/scons/scons-%realversion.tar.gz
Requires: python3

%prep
%setup -n scons-%realversion

%build
python3 setup.py build

%install
python3 setup.py install --prefix=%i
find %i -name '*.egg-info' -exec rm {} \;
%define drop_files %i/man

# replace all instances of #!/path/bin/python into proper format
%py3PathRelocation

# Generate dependencies-setup.{sh,csh} so init.{sh,csh} picks full environment.
%addDependency

%post
%{relocateConfig}etc/profile.d/dependencies-setup.*sh
