### RPM cms py3-dbs3-client 3.16.0
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}
## INITENV +PATH PYTHONPATH %i/x${PYTHON_LIB_SITE_PACKAGES}
## INITENV SET DBS3_CLIENT_ROOT %i/
## INITENV SET DBS3_CLIENT_VERSION %v
## INITENV ALIAS dbs python $DBS3_CLIENT_ROOT/bin/dbs.py

%define webdoc_files %{installroot}/%{pkgrel}/doc/
# Source0: git://github.com/dmwm/DBS.git?obj=master/%{realversion}&export=DBS&output=/%{n}.tar.gz
Source0: git://github.com/dmwm/DBS.git?obj=py3-dbs3-client&export=DBS&output=/%{n}.tar.gz
Requires: python3 py3-dbs3-pycurl-client
# BuildRequires: py3-sphinx

%prep
%setup -D -T -b 0 -n DBS

%build
python3 setup.py build_system -s dbs-client
%install
mkdir -p %i/etc/profile.d %i/{x,}{bin,lib,data,doc} %i/{x,}$PYTHON_LIB_SITE_PACKAGES
python3 setup.py install_system -s dbs-client --prefix=%i
find %i -name '*.egg-info' -exec rm {} \;

%files
%{installroot}/%{pkgrel}/
%exclude %{installroot}/%{pkgrel}/doc
## SUBPACKAGE webdoc
