### RPM cms sitedb 1.2.3
## INITENV +PATH PYTHONPATH %i/lib/python`echo $PYTHON_VERSION | cut -d. -f 1,2`/site-packages 

%define moduleName WEBTOOLS
%define exportName WEBTOOLS
%define cvstag SiteDBv1-slc5-v3 
%define cvsserver cvs://:pserver:anonymous@cmscvs.cern.ch:2401/cvs_server/repositories/CMSSW?passwd=AA_:yZZ3e

Source: %cvsserver&strategy=checkout&module=%{moduleName}&nocache=true&export=%{exportName}&tag=-r%{cvstag}&output=/%{moduleName}.tar.gz

Requires: python cherrypy py2-cheetah yui sqlite zlib py2-pysqlite expat openssl bz2lib db4 gdbm py2-cx-oracle py2-formencode py2-pycrypto oracle webtools oracle-env 

Provides: perl(CGI) 
Provides: perl(Crypt::CBC) 
Provides: perl(SecurityModule) 
Provides: perl(DBI)

%prep
%setup -n %{moduleName}

%build

%install
mkdir -p %i/lib/python`echo $PYTHON_VERSION | cut -d. -f1,2`/site-packages/Applications
rm -rf Applications/SiteDB/Utilities/MigrateSites
cp -r Applications/SiteDB %i/lib/python`echo $PYTHON_VERSION | cut -d. -f1,2`/site-packages/Applications
mkdir -p %i/lib/python`echo $PYTHON_VERSION | cut -d. -f1,2`/site-packages/Applications/SiteDB/csv

# Dependencies environment setup
rm -rf %i/etc/profile.d
mkdir -p %i/etc/profile.d
for x in %pkgreqs; do
  case $x in /* ) continue ;; esac
  p=%{instroot}/%{cmsplatf}/$(echo $x | sed 's/\([^+]*\)+\(.*\)+\([A-Z0-9].*\)/\1 \2 \3/' | tr ' ' '/')
  echo ". $p/etc/profile.d/init.sh" >> %i/etc/profile.d/dependencies-setup.sh
  echo "source $p/etc/profile.d/init.csh" >> %i/etc/profile.d/dependencies-setup.csh
done


%post
# The relocation below is also needed in case of dependencies
%{relocateConfig}etc/profile.d/dependencies-setup.sh
%{relocateConfig}etc/profile.d/dependencies-setup.csh

