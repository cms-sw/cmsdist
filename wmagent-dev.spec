### RPM cms wmagent-dev 0.9.83

# This is a meta-package to group development tool dependencies
Requires: wmagent rotatelogs pystack wmcore-devtools

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
    echo "test X\$$root != X || source $r/etc/profile.d/init.csh" >> %i/etc/profile.d/dependencies-setup.csh
  fi
done

%post
# The relocation is also needed because of dependencies
%{relocateConfig}etc/profile.d/dependencies-setup.*sh
