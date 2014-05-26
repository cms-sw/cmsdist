### RPM cms lifecycle-das 1.0.12
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}
Source0: https://github.com/dmwm/LifeCycle/archive/%{realversion}.tar.gz
Requires: python PHEDEX-lifecycle

%prep
%setup -D -T -b 0 -n LifeCycle-%{realversion}

%build

%install
cd LifeCycleDAS
mkdir -p %i/$PYTHON_LIB_SITE_PACKAGES/LifeCycleDAS
cp -r *.py utils %i/$PYTHON_LIB_SITE_PACKAGES/LifeCycleDAS

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
