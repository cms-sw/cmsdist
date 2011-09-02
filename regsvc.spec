### RPM cms regsvc 0.0.1
%define version V_0_1

#Source: svn://svn.cern.ch/reps/CMSDMWM/RegSvc/tags/%{v}?scheme=svn+ssh&strategy=export&module=RegSvc&output=/src.tar.gz
Source: svn://svn.cern.ch/reps/CMSDMWM/RegSvc/trunk/?scheme=svn+ssh&strategy=export&module=RegSvc&output=/src_RegSvc.tar.gz

Requires: couchdb

%prep
%setup -n RegSvc

%build

%install
mkdir -p %i/RegSvc/couchapps
cp -rp %_builddir/RegSvc/src/couchapps %i/RegSvc/couchapps

# Generate dependencies-setup.{sh,csh} so init.{sh,csh} picks full environment.
rm -rf %i/etc/profile.d
mkdir -p %i/etc/profile.d
for tool in $(echo %{requiredtools} | sed -e's|\s+| |;s|^\s+||'); do
  root=$(echo $tool | tr a-z- A-Z_)_ROOT; eval r=\$$root
  if [ X"$r" != X ] && [ -r "$r/etc/profile.d/init.sh" ]; then
    echo "test X\$$root != X || . $r/etc/profile.d/init.sh" >> %i/etc/profile.d/dependencies-setup.sh
    echo "test X\$$root != X || source $r/etc/profile.d/init.csh" >> %i/etc/profile.d/dependencies-setup.csh
  fi
done

%post
%{relocateConfig}etc/profile.d/dependencies-setup.*sh
