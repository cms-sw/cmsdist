### RPM cms sreadiness r178
## INITENV +PATH PYTHONPATH %i/lib/python`echo $PYTHON_VERSION | cut -d. -f 1,2`/site-packages 

%define svnrev %(echo %realversion|tr -d 'r')
Source1: svn://svn.cern.ch/reps/cmsfomon/SiteReadiness/trunk@%svnrev?scheme=svn+ssh&strategy=export&module=SiteReadiness&output=/srsrc.tar.gz
Requires: python py2-matplotlib py2-numpy py2-pyxml


%prep
%setup -T -b 1 -n SiteReadiness

%build

%install
mkdir %i/bin
cp -rp %_builddir/SiteReadiness/* %i/bin

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
