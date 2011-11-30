### RPM cms CmsProjectBuilder 1.40
## INITENV +PATH PYTHONPATH %i/lib/python`echo $PYTHON_VERSION | cut -f1,2 -d.`/site-packages
%define svnversion %realversion

Source: svn://svn.cern.ch/reps/CMSIntBld/tags/CmsProjectBuilder/V00-00-01/?scheme=svn+ssh&strategy=export&module=CmsProjectBuilder&output=/CmsProjectBuilder.tar.gz 


Requires: python py2-simplejson py2-sqlalchemy py2-httplib2

%prep
%setup -n CmsProjectBuilder

%build
python setup2.py build 

%install
python setup2.py install --prefix=%i
python setup2.py install_data --install-dir=%i
egrep -r -l '^#!.*python' %i | xargs perl -p -i -e 's{^#!.*python.*}{#!/usr/bin/env python}'
find %i -name '*.egg-info' -exec rm {} \;
mkdir -p %{i}/workdir

# Generate dependencies-setup.{sh,csh} so init.{sh,csh} picks full environment.
mkdir -p %i/etc/profile.d
: > %i/etc/profile.d/dependencies-setup.sh
: > %i/etc/profile.d/dependencies-setup.csh
for tool in $(echo %{requiredtools} | sed -e's|\s+| |;s|^\s+||'); do
  root=$(echo $tool | tr a-z- A-Z_)_ROOT; eval r=\$$root
  if [ X"$r" != X ] && [ -r "$r/etc/profile.d/init.sh" ]; then
    echo "test X\$$root != X || . $r/etc/profile.d/init.sh" >> %i/etc/profile.d/dependencies-setup.sh
    echo "test X\$$root != X || source $r/etc/profile.d/init.csh" >> %i/etc/profile.d/dependencies-setup.csh
  fi
done

%post
%{relocateConfig}etc/profile.d/dependencies-setup.*sh
