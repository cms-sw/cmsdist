### RPM external srmcp 1.9.2_4
## INITENV +PATH PATH %i/bin:%i/sbin
## INITENV SET SRM_PATH %i

%define realv %(echo %realversion | tr "_" "-")
Source: http://www.dcache.org/downloads/1.9/dcache-srmclient-%realv.noarch.rpm
Requires: java-jdk

%prep
rpm2cpio %{_sourcedir}/dcache-srmclient-%realv.noarch.rpm | cpio -ivd 

%build

%install
mv %{_builddir}/opt/d-cache/srm/* %i

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
