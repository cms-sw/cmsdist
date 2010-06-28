### RPM external couchapp 0.6.2

Source0: http://github.com/couchapp/couchapp/tarball/0.6.2
Requires: python py2-setuptools

%prep
cd %_builddir
tar xvzf %_sourcedir/0.6.2
mv %_builddir/couchapp-couchapp-eecd2b8 %_builddir/couchapp-0.6.2 

%build

%install
cd %_builddir/couchapp-0.6.2
python setup.py install --prefix=%i
cp -rp %_builddir/couchapp-0.6.2/* %i/
rm -rf %i/couchapp # exclude the 'source' dir

# This will generate the correct dependencies-setup.sh/dependencies-setup.csh
# using the information found in the Requires statements of the different
# specs and their dependencies.
rm -rf %i/etc/profile.d
mkdir -p %i/etc/profile.d
for x in %pkgreqs; do
  case $x in /* ) continue ;; esac
  p=%{instroot}/%{cmsplatf}/$(echo $x | sed 's/\([^+]*\)+\(.*\)+\([A-Z0-9].*\)/\1 \2 \3/' | tr ' ' '/')
  echo ". $p/etc/profile.d/init.sh" >> %i/etc/profile.d/dependencies-setup.sh
  echo "source $p/etc/profile.d/init.csh" >> %i/etc/profile.d/dependencies-setup.csh
done

%post
%{relocateConfig}etc/profile.d/dependencies-setup.sh
%{relocateConfig}etc/profile.d/dependencies-setup.csh

