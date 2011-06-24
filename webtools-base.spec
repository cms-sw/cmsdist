### RPM cms webtools-base 0.1.21
## INITENV +PATH PYTHONPATH %i/$PYTHON_LIB_SITE_PACKAGES

%define moduleName WEBTOOLS
%define cvstag V01-03-43
%define cvsserver cvs://:pserver:anonymous@cmscvs.cern.ch:2401/cvs_server/repositories/CMSSW?passwd=AA_:yZZ3e
Source: %cvsserver&strategy=checkout&module=%{moduleName}&nocache=true&export=%{moduleName}&tag=-r%{cvstag}&output=/%{moduleName}.tar.gz

Requires: python webtools rotatelogs

%prep
%setup -n %{moduleName}

%build

%install
mkdir -p %i/$PYTHON_LIB_SITE_PACKAGES/Applications

# Copy only the 'base' application
cp -r Applications/base %i/$PYTHON_LIB_SITE_PACKAGES/Applications

# Generate .pyc files.
python -m compileall %i/$PYTHON_LIB_SITE_PACKAGES || true

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

