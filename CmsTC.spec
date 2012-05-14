### RPM cms CmsTC CmsTC_1_4_3
## INITENV +PATH PYTHONPATH %i 
%define moduleName %n
%define exportName %n
%define cvstag %realversion
%define cvsserver cvs://:pserver:anonymous@cmssw.cvs.cern.ch:2401/cvs_server/repositories/CMSSW?passwd=AA_:yZZ3e
Source: %cvsserver&strategy=checkout&module=%{moduleName}&nocache=true&export=%{exportName}&tag=-r%{cvstag}&output=/%{moduleName}.tar.gz
#Requires: python cherrypy py2-cx-oracle rotatelogs py2-cheetah  py2-pyopenssl graphviz
Requires: python cherrypy py2-cx-oracle rotatelogs py2-cheetah py2-pyopenssl
 
%prep
%setup -n %{moduleName}

%build
python -c 'import compileall; compileall.compile_dir(".",force=True)'

%install
cp -pr * %i
egrep -r -l '^#!.*python' %i | xargs perl -p -i -e 's{^#!.*python.*}{#!/usr/bin/env python}'

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
