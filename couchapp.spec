### RPM external couchapp 0.6.2
## INITENV +PATH PYTHONPATH %i/lib/python`echo $PYTHON_VERSION | cut -f1,2 -d.`/site-packages

# Don't need to specify sources since it installs using easy_install
Requires: python py2-setuptools

%prep
#cd %_builddir
#tar xvzf %_sourcedir/0.6.2
#mv %_builddir/couchapp-couchapp-eecd2b8 %_builddir/couchapp-0.6.2 
#mv %_sourcedir/ez_setup.py %_builddir/couchapp-0.6.2

%build

%install
#cd %_builddir/couchapp-0.6.2
#python setup.py install --prefix=%i
#python ez_setup.py -U setuptools --prefix=%i
#cp -rp %_builddir/couchapp-0.6.2/* %i/
#rm -rf %i/couchapp # exclude the 'source' dir
export PYTHONPATH=$PYTHONPATH:%i/lib/python`echo $PYTHON_VERSION | cut -f1,2 -d.`/site-packages
mkdir -p %i/lib/python`echo $PYTHON_VERSION | cut -f1,2 -d.`/site-packages
easy_install --prefix %i -U couchapp

# Fixes to static path's to python left by the easy_install installation
perl -p -i -e "s|#!.*/usr/bin/python|#!/usr/bin/env python|" %i/lib/python`echo $PYTHON_VERSION | cut -f1,2 -d.`/site-packages/Couchapp-0.6.2-py2.6.egg/couchapp/hooks/compress/jsmin.py
perl -p -i -e "s|#!.*/python|#!/usr/bin/env python|" %i/bin/couchapp

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

