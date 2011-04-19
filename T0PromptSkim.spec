### RPM cms T0PromptSkim 1.0.8
## INITENV +PATH PYTHONPATH %i/lib/python`echo $PYTHON_VERSION | cut -d. -f 1,2`/site-packages 
%define wmcver 0.7.4
%define moduleName T0
%define exportName T0
%define cvstag T0PromptSkim-1_0_8
%define cvsserver cvs://:pserver:anonymous@cmscvs.cern.ch:2401/cvs_server/repositories/CMSSW?passwd=AA_:yZZ3e
%define svnserver svn://svn.cern.ch/reps/CMSDMWM
Source0: %svnserver/WMCore/tags/%{wmcver}?scheme=svn+ssh&strategy=export&module=WMCore&output=/wmcore_t0promptskim.tar.gz
Source1: %cvsserver&strategy=checkout&module=%{moduleName}&nocache=true&export=%{exportName}&tag=-r%{cvstag}&output=/T0PromptSkim.tar.gz
Requires: py2-cx-oracle

%prep
%setup -T -b 0 -n WMCore
%setup -D -T -b 1 -n %{moduleName}

%build
cd ../WMCore
python setup.py build_system -s wmc-web

%install
cd ../WMCore
python setup.py install_system -s wmc-web --prefix=%i
cd ../%{moduleName}
tar -C src/python -cf - \
  T0/ConfDB T0/DataStructs T0/RunConfigCache \
  T0/GenericTier0/Tier0DB.py T0/Globals.py \
  T0/State/Database/Reader \
  T0/State/Database/Writer |
  tar -C %i/lib/python*/site-packages -xvvf -
find %i/lib/python*/site-packages/T0 -type d -exec touch {}/__init__.py \;
find %i -name '*.egg-info' -exec rm {} \;

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
