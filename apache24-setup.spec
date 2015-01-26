### RPM cms apache24-setup 3.6
Source: git://github.com/dmwm/apache-conf?obj=master/%{realversion}&export=%n&output=/%n.tar.gz
Requires: apache24

%prep
%setup -n %n 

%build

%install
mkdir -p %i/{bin,etc/env.d,etc/profile.d}
mv mkserver %i/bin/
sed -i -e "s,APACHE2_ROOT,APACHE24_ROOT,g" %i/bin/mkserver
ln -sf ../profile.d/init.sh %i/etc/env.d/00-core-server.sh

# Generate dependencies-setup.{sh,csh} so init.{sh,csh} picks full environment.
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
