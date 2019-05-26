### RPM cms dbs3-client 3.9.1
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}
## INITENV +PATH PYTHONPATH %i/x${PYTHON_LIB_SITE_PACKAGES}
## INITENV SET DBS3_CLIENT_ROOT %i/
## INITENV SET DBS3_CLIENT_VERSION %v
## INITENV ALIAS dbs python $DBS3_CLIENT_ROOT/bin/dbs.py

%define webdoc_files %{installroot}/%{pkgrel}/doc/
Source0: git://github.com/dmwm/DBS.git?obj=master/%{realversion}&export=DBS&output=/%{n}.tar.gz
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

%files
%{installroot}/%{pkgrel}/
%exclude %{installroot}/%{pkgrel}/doc
## SUBPACKAGE webdoc
