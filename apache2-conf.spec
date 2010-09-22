### RPM cms apache2-conf 3.1
Source: svn://svn.cern.ch/reps/CMSDMWM/HTTPGroup/tags/%{realversion}?scheme=svn+ssh&strategy=export&module=HTTPGroup&output=/conf.tar.gz
Requires: apache2

%prep
%setup -n HTTPGroup/ApacheConf

%build

%install
mkdir -p %i/{bin,etc/env.d,etc/profile.d}
mv mkserver %i/bin/
mv archive-log-files %i/
ln -sf ../profile.d/init.sh %i/etc/env.d/00-core-server.sh

# Generate dependencies-setup.{sh,csh} so init.{sh,csh} picks full environment.
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
