### RPM cms security-module CERNOIDv01

%define pythonv %(echo $PYTHON_VERSION | cut -d. -f 1,2)

# Needs python >= 2.6
Requires: openid-client wmcore
Source: cvs://:pserver:anonymous@cmscvs.cern.ch:2401/cvs_server/repositories/CMSSW?passwd=AA_:yZZ3e&strategy=export&nocache=true&module=WEBTOOLS/Applications/Security&export=%{n}&tag=-r%{v}&output=/%{n}.tar.gz


%prep
%setup -n %{n}

%build

%install
cp -p %_builddir/%{n}/Applications/Security/* %i/
#python setup.py install --prefix=%i # Not yet available for the OpenID server...

# Perhaps the following is needed to fix python source headers
perl -p -i -e "s|^#!.*python(.*)|#!/usr/bin/env python$1|" `grep -r -e "^#\!.*python.*" %i | cut -d: -f1`

# The following lines are not necessary because they are assumed by default
#%files
#%i/

