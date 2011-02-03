### RPM cms CmsTC 0.0.1
## INITENV +PATH PYTHONPATH %i/lib/python`echo $PYTHON_VERSION | cut -d. -f 1,2`/site-packages 
%define moduleName CmsTC
%define exportName CmsTC
%define cvstag CmsTC_0_0_1
%define cvsserver cvs://:pserver:anonymous@cmscvs.cern.ch:2401/cvs_server/repositories/CMSSW?passwd=AA_:yZZ3e
Source: %cvsserver&strategy=checkout&module=%{moduleName}&nocache=true&export=%{exportName}&tag=-r%{cvstag}&output=/%{moduleName}.tar.gz
Requires: python cherrypy py2-cx-oracle rotatelogs py2-mako py2-setuptools

%prep
%setup -n %{moduleName}

%build
#python setup.py build

%install
mkdir -p %i/lib/python`echo $PYTHON_VERSION | cut -d. -f 1,2`/site-packages
#PYTHONPATH=${PYTHONPATH}:%i/lib/python`echo $PYTHON_VERSION | cut -d. -f 1,2`/site-packages
##python setup.py install --prefix=%i
cp -pr * %i/lib/python`echo $PYTHON_VERSION | cut -d. -f 1,2`/site-packages
egrep -r -l '^#!.*python' %i | xargs perl -p -i -e 's{^#!.*python.*}{#!/usr/bin/env python}'
find %i -name '*.egg-info' -exec rm {} \;

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
