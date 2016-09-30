### RPM cms PhedexReplicaMonitoring v00.00.05
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}
%define pkg PhedexReplicaMonitoring
Source: git://github.com/aurimasrep/PhedexReplicaMonitoring?obj=master/%realversion&export=%pkg&output=/%pkg.tar.gz
Requires: python py2-py4j java-jdk elasticsearch elasticsearch-hadoop kibana rotatelogs
BuildRequires: py2-sphinx

# RPM macros documentation
# http://www.rpm.org/max-rpm/s1-rpm-inside-macros.html
%prep
%setup -b 0 -n %pkg

%build
#cd %pkg

%install
mkdir -p %i/${PYTHON_LIB_SITE_PACKAGES}
mkdir -p %i/bin
cp -r src/python/* %i/${PYTHON_LIB_SITE_PACKAGES}
cp src/scripts/*.sh %i/bin
cp -r data %i/
cp -r etc %i/

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
