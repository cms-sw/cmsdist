### RPM cms dbs3-client 3.3.120
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}
## INITENV +PATH PYTHONPATH %i/x${PYTHON_LIB_SITE_PACKAGES}
## INITENV SET DBS3_CLIENT_ROOT %i/
## INITENV SET DBS3_CLIENT_VERSION %v
## INITENV ALIAS dbs python $DBS3_CLIENT_ROOT/bin/dbs.py

%define webdoc_files %{installroot}/%{pkgrel}/doc/
%define tag %(echo %{realversion} | sed 's/[.]/_/g; s/^/DBS_/')
Source0: git://github.com/dmwm/DBS.git?obj=master/%{tag}&export=DBS&output=/%{n}.tar.gz
Requires: python py2-cjson dbs3-pycurl-client
BuildRequires: py2-sphinx

%prep
%setup -D -T -b 0 -n DBS

%build
python setup.py build_system -s dbs-client
%install
mkdir -p %i/etc/profile.d %i/{x,}{bin,lib,data,doc} %i/{x,}$PYTHON_LIB_SITE_PACKAGES
python setup.py install_system -s dbs-client --prefix=%i
find %i -name '*.egg-info' -exec rm {} \;
cp %i/examples/DataOpsScripts/*.py %i/bin

# create wrapper script
mkdir -p %i/etc
pver=$PYTHON_LIB_SITE_PACKAGES
cat << \EOF > %i/etc/dbsenv
#!/bin/sh
# Clean-up CMSSW environment
if [ -f %{instroot}/common/scram ]; then
    eval `%{instroot}/common/scram unsetenv -sh`
fi
# Sourcing dasclient environment
SHARED_ARCH=`%{instroot}/common/cmsos`
LATEST_VERSION=`ls %{instroot}/${SHARED_ARCH}_*/%{pkgcategory}/%{pkgname} | sed 's|.*/%{pkgcategory}/%{pkgname}/||' | sort | tail -1`
source %{instroot}/${SHARED_ARCH}_*/%{pkgcategory}/%{pkgname}/${LATEST_VERSION}/etc/profile.d/init.sh
EOF

chmod +x %i/etc/dbsenv

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
%{relocateConfig}etc/dbsenv

# copy wrapper script into common if latest version is same as this version
mkdir -p $RPM_INSTALL_PREFIX/common
if [ ! -f $RPM_INSTALL_PREFIX/common/dbsenv ]; then
  cp ${RPM_INSTALL_PREFIX}/%{pkgrel}/etc/dbsenv $RPM_INSTALL_PREFIX/common/
fi
if [ "`ls ${RPM_INSTALL_PREFIX}/*/%{pkgcategory}/%{pkgname}/v*/etc/profile.d/init.sh | sed 's|.*/%{pkgcategory}/%{pkgname}/||;s|/etc/profile.d/init.sh||' | sort | tail -1`" = "%v" ] ; then
  /bin/cp -f ${RPM_INSTALL_PREFIX}/%{pkgrel}/etc/dbsenv $RPM_INSTALL_PREFIX/common/dbsenv.tmp
  mv $RPM_INSTALL_PREFIX/common/dbsenv.tmp $RPM_INSTALL_PREFIX/common/dbsenv
fi

%files
%{installroot}/%{pkgrel}/
%exclude %{installroot}/%{pkgrel}/doc
## SUBPACKAGE webdoc
