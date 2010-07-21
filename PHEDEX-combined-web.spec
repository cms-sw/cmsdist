### RPM cms PHEDEX-combined-web 2

# This is a fake spec whose only job is to build PHEDEX-web and
# PHEDEX-datasvc on a combined platform of dependencies

Requires: PHEDEX-web PHEDEX-datasvc PHEDEX-webapp

%prep
cd %_builddir
%build
%install
mkdir -p %{i}/bin
mkdir -p %{i}/lib
mkdir -p %{i}/etc/profile.d

(echo "#!/bin/sh"; \
 echo "source $PHEDEX_WEB_ROOT/etc/profile.d/init.sh"; \
 echo "source $PHEDEX_DATASVC_ROOT/etc/profile.d/init.sh"; \
 ) > %{i}/etc/profile.d/dependencies-setup.sh

(echo "#!/bin/tcsh"; \
 echo "source $PHEDEX_WEB_ROOT/etc/profile.d/init.csh"; \
 echo "source $PHEDEX_DATASVC_ROOT/etc/profile.d/init.csh"; \
 ) > %{i}/etc/profile.d/dependencies-setup.csh

%post
%{relocateConfig}etc/profile.d/dependencies-setup.sh
%{relocateConfig}etc/profile.d/dependencies-setup.csh
