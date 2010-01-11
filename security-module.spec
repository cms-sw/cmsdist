### RPM cms security-module V00_00_00

%define pythonv %(echo $PYTHON_VERSION | cut -d. -f 1,2)

# Needs python >= 2.6
Requires: wmcore-webtools
Source: cvs://:pserver:anonymous@cmscvs.cern.ch:2401/cvs_server/repositories/CMSSW?passwd=AA_:yZZ3e&strategy=export&nocache=true&module=WEBTOOLS/Applications/Security&export=%{n}&tag=-r%{v}&output=/%{n}.tar.gz


%prep
%setup -n %{n}

%build

%install
cp -rp %_builddir/%{n}/Applications/Security/* %i/
#python setup.py install --prefix=%i # Not yet available for the OpenID server...

rm -rf %i/etc/profile.d
# Perhaps the following is needed to fix python source headers
#perl -p -i -e "s|^#!.*python(.*)|#!/usr/bin/env python$1|" `grep -r -e "^#\!.*python.*" %i | cut -d: -f1`

# Copy dependencies to dependencies-setup.sh
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

