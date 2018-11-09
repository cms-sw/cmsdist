### RPM cms webtools 1.3.48
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}
## INITENV +PATH PERL5LIB %i/lib/perl

%define gittag V01-03-48
Source: git://github.com/geneguvo/webtools?obj=master/%gittag&export=%n&output=/%n.tar.gz

Requires: python cherrypy py2-cheetah yui sqlite zlib py2-pysqlite expat openssl bz2lib db4 gdbm py2-cx-oracle py2-formencode py2-pycrypto oracle beautifulsoup py2-sqlalchemy oracle-env py2-pyOpenSSL
Requires: p5-crypt-cbc p5-crypt-blowfish

Provides: perl(SecurityModule) 

%prep
%setup -n %n

%build

%install
mkdir -p %i/{etc,bin} %i/$PYTHON_LIB_SITE_PACKAGES %i/lib/perl

cp -r SecurityModule/perl/lib/* %i/lib/perl
rm -rf Applications Configuration Tools/StartupScripts SecurityModule/perl
cp -r * %i/$PYTHON_LIB_SITE_PACKAGES
cp cmsWeb %i/bin

# Generate .pyc files.
python -m compileall %i/$PYTHON_LIB_SITE_PACKAGES || true

# Generate dependencies-setup.{sh,csh} so init.{sh,csh} picks full environment.
mkdir -p %i/etc/profile.d
: > %i/etc/profile.d/dependencies-setup.sh
: > %i/etc/profile.d/dependencies-setup.csh
for tool in $(echo %{requiredtools} | sed -e's|\s+| |;s|^\s+||'); do
  root=$(echo $tool | tr a-z- A-Z_)_ROOT; eval r=\$$root
  if [ X"$r" != X ] && [ -r "$r/etc/profile.d/init.sh" ]; then
    echo "test X\$$root != X || . $r/etc/profile.d/init.sh" >> %i/etc/profile.d/dependencies-setup.sh
    echo "test X\$?$root = X1 || source $r/etc/profile.d/init.csh" >> %i/etc/profile.d/dependencies-setup.csh
  fi
done

%post
%{relocateConfig}etc/profile.d/dependencies-setup.*sh
perl -p -i -e "s!\@RPM_INSTALL_PREFIX\@!$RPM_INSTALL_PREFIX/%pkgrel!" $RPM_INSTALL_PREFIX/%pkgrel/bin/cmsWeb

