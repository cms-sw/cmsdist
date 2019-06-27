### RPM cms das_client v03.01.00
%define pkg DAS

Source0: git://github.com/dmwm/DAS?obj=master/%realversion&export=%pkg&output=/%pkg.tar.gz
Requires: python

# RPM macros documentation
# http://www.rpm.org/max-rpm/s1-rpm-inside-macros.html
%prep
%setup -c
%setup -T -D -a 0

%build

%install
mkdir -p %i/bin
cp %{pkg}/src/python/DAS/tools/das_client.py %i/bin

# create wrapper script
mkdir -p %i/etc
cat << \EOF > %i/etc/das_client
#!/bin/sh
# VERSION:%{cmsplatf}/%{v}
# Clean-up CMSSW environment
eval `scram unsetenv -sh 2>/dev/null`
# Sourcing dasclient environment
SHARED_ARCH=`cmsos`
LATEST_VERSION=`cd %{instroot}; ls ${SHARED_ARCH}_*/%{pkgcategory}/%{pkgname}/v*/etc/profile.d/init.sh | sed 's|.*/%{pkgcategory}/%{pkgname}/||' | sort | tail -1`
DAS_ENV=`ls %{instroot}/${SHARED_ARCH}_*/%{pkgcategory}/%{pkgname}/${LATEST_VERSION} | sort | tail -1`
source $DAS_ENV
if [ $# == 0 ] || [ "$1" == "--help" ] || [ "$1" == "-help" ]
then
    $DAS_CLIENT_ROOT/bin/das_client.py --help | sed 's/das_client.py/das_client/'
else
    $DAS_CLIENT_ROOT/bin/das_client.py "$@"
fi
EOF

chmod +x %i/etc/das_client

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
%{relocateConfig}etc/das_client

# copy wrapper script into common if latest version is same as this version
mkdir -p $RPM_INSTALL_PREFIX/common
if [ "`ls ${RPM_INSTALL_PREFIX}/*/%{pkgcategory}/%{pkgname}/v*/etc/profile.d/init.sh | sed 's|.*/%{pkgcategory}/%{pkgname}/||;s|/etc/profile.d/init.sh||' | sort | tail -1`" = "%v" ] ; then
  /bin/cp -f ${RPM_INSTALL_PREFIX}/%{pkgrel}/etc/das_client $RPM_INSTALL_PREFIX/common/das_client.tmp
  mv $RPM_INSTALL_PREFIX/common/das_client.tmp $RPM_INSTALL_PREFIX/common/das_client
fi

#Create overrides/bin directory (newly supported by SCRAM)
#and make sure that das_client.py script points to das_cleint wrapper
mkdir -p $RPM_INSTALL_PREFIX/share/overrides/bin
[ -e $RPM_INSTALL_PREFIX/share/overrides/bin/das_client.py ] || ln -sf ../../../common/das_client $RPM_INSTALL_PREFIX/share/overrides/bin/das_client.py
# bla bla
