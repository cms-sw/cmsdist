### RPM cms pkgtools 0.6.0 
# This generates an rpm for aptinstaller, install.sh, etc. etc.
Requires: cms-env apt git
%define moduleName PKGTOOLS
%define exportName PKGTOOLS 
%define cvstag V00-06-08
%define cvsserver cvs://:pserver:anonymous@cmscvs.cern.ch:2401/cvs_server/repositories/CMSSW?passwd=AA_:yZZ3e
Source: %cvsserver&strategy=checkout&module=%{moduleName}&nocache=true&export=%{exportName}&tag=-r%{cvstag}&output=/PKGTOOLS.tar.gz

%prep
%setup -n PKGTOOLS 
%build
%install
mkdir -p %{i}/bin
ln -sf %pkgrel/etc/profile.d/init.sh %{instroot}/pkgtools-init.sh
install -m 755 cmsBuild %{i}/bin/cmsBuild
install -m 755 downloadOracle.sh %{i}/bin/downloadOracle.sh

rm -rf %i/etc/profile.d
mkdir -p %i/etc/profile.d
echo '#!/bin/sh' > %{i}/etc/profile.d/dependencies-setup.sh
echo '#!/bin/tcsh' > %{i}/etc/profile.d/dependencies-setup.csh
echo requiredtools `echo %{requiredtools} | sed -e's|\s+| |;s|^\s+||'`
for tool in `echo %{requiredtools} | sed -e's|\s+| |;s|^\s+||'`
do
    case X$tool in
        Xdistcc|Xccache )
        ;;
        * )
            toolcap=`echo $tool | tr a-z- A-Z_`
            eval echo ". $`echo ${toolcap}_ROOT`/etc/profile.d/init.sh" >> %{i}/etc/profile.d/dependencies-setup.sh
            eval echo "source $`echo ${toolcap}_ROOT`/etc/profile.d/init.csh" >> %{i}/etc/profile.d/dependencies-setup.csh
        ;;
    esac
done
perl -p -i -e 's|\. /etc/profile\.d/init\.sh||' %{i}/etc/profile.d/dependencies-setup.sh
perl -p -i -e 's|source /etc/profile\.d/init\.csh||' %{i}/etc/profile.d/dependencies-setup.csh

%post
%{relocateConfig}/etc/profile.d/dependencies-setup.sh
%{relocateConfig}/etc/profile.d/dependencies-setup.csh
%files
%{i}
%{instroot}/pkgtools-init.sh
