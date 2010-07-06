### RPM cms security-module V00_00_01

Requires: wmcore-webtools
Source: cvs://:pserver:anonymous@cmscvs.cern.ch:2401/cvs_server/repositories/CMSSW?passwd=AA_:yZZ3e&strategy=export&nocache=true&module=WEBTOOLS/Applications/Security&export=%{n}&tag=-r%{v}&output=/%{n}.tar.gz
Obsoletes: cms+security-module+V00_00_00
Obsoletes: cms+security-module+V00_00_00-cmp
Obsoletes: cms+security-module+V00_00_00-cmp2



%prep
%setup -n %{n}

%build

%install
cp -rp %_builddir/%{n}/Applications/Security/* %i/
#python setup.py install --prefix=%i # Not yet available for the OpenID server...

# Copy dependencies to dependencies-setup.sh
rm -rf %i/etc/profile.d
mkdir -p %i/etc/profile.d
for x in %pkgreqs; do
  case $x in /* ) continue ;; esac
  p=%{instroot}/%{cmsplatf}/$(echo $x | sed 's/\([^+]*\)+\(.*\)+\([A-Z0-9].*\)/\1 \2 \3/' | tr ' ' '/')
  echo ". $p/etc/profile.d/init.sh" >> %i/etc/profile.d/dependencies-setup.sh
  echo "source $p/etc/profile.d/init.csh" >> %i/etc/profile.d/dependencies-setup.csh
done

%post
%{relocateConfig}etc/profile.d/dependencies-setup.sh
%{relocateConfig}etc/profile.d/dependencies-setup.csh

