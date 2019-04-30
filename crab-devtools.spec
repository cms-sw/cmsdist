### RPM cms crab-devtools 1.1

# This is a meta-package to group development tool dependencies and all the crab3 packages
Requires: crabclient crabserver crabtaskworker crabcache yuicompressor
Requires: py2-coverage py2-pylint py2-nose py2-sphinx py2-mox py2-future

%prep
%build
%install

# Generate dependencies-setup.{sh,csh} so init.{sh,csh} picks full environment.
rm -rf %i/etc/profile.d
mkdir -p %i/etc/profile.d
for tool in $(echo %{requiredtools} | sed -e's|\s+| |;s|^\s+||'); do
  root=$(echo $tool | tr a-z- A-Z_)_ROOT; eval r=\$$root
  if [ X"$r" != X ] && [ -r "$r/etc/profile.d/init.sh" ]; then
    echo "test X\$$root != X || . $r/etc/profile.d/init.sh" >> %i/etc/profile.d/dependencies-setup.sh
    echo "test X\$?$root = X1 || source $r/etc/profile.d/init.csh" >> %i/etc/profile.d/dependencies-setup.csh
  fi
done

%post
# The relocation is also needed because of dependencies
%{relocateConfig}etc/profile.d/dependencies-setup.*sh
