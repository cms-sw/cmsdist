### RPM cms dbs3-lifecycle 0.0.1
## INITENV +PATH PYTHONPATH %i/$PYTHON_LIB_SITE_PACKAGES
## INITENV +PATH PYTHONPATH %i/x$PYTHON_LIB_SITE_PACKAGES
## INITENV SET DBS3_LIFECYCLE_ROOT %i/

%define gitserver https://nodeload.github.com 
Source0: %gitserver/giffels/LifeCycleTests/tarball/%{realversion}
Requires: python dbs3-client lifecycle-dataprovider PHEDEX-lifecycle

%prep
%setup -c 
# move github directory
mv giffels-LifeCycleTests* LifeCycleTests
%setup -D -T -a 0

%build
cd LifeCycleTests
python setup.py build_system -s LifeCycleTests
%install
mkdir -p %i/etc/profile.d %i/{x,}{bin,lib,data,doc} %i/{x,}$PYTHON_LIB_SITE_PACKAGES
cd LifeCycleTests
python setup.py install_system -s LifeCycleTests --prefix=%i
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

%files
%{installroot}/%{pkgrel}/
