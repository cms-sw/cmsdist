### RPM cms dls-client DLS_1_1_3
## INITENV +PATH PATH %{i}/Client/bin
## INITENV +PATH PYTHONPATH %{i}/Client/lib

Source: git://github.com/geneguvo/dls-client?obj=master/%realversion&export=%n&output=/%n.tar.gz
Requires: python dbs-client py2-pyxml

%prep
%setup -n %n
perl -p -i -e "s|#!/usr/bin/python|#!/usr/bin/env python|" $(find .)
%build
%install
#
cd Client
make %{makeprocesses}
mkdir -p  %{i}/Client
cp -r lib %{i}/Client/.
cp -r bin %{i}/Client/.
cp README %{i}/Client/.
#cp -r etc %{i}/Client/.
python -m compileall %i/Client || true

mkdir -p %{i}/etc/profile.d
 
echo "test"
(echo "#!/bin/sh"; \
 echo "source $PYTHON_ROOT/etc/profile.d/init.sh"; \
 echo "source $PY2_PYXML_ROOT/etc/profile.d/init.sh"; \
 echo "source $DBS_CLIENT_ROOT/etc/profile.d/init.sh"; 
 echo "if [ -f $DBS_CLIENT_ROOT/lib/Clients/Python/DBSAPI/dbs.config ]; then";
 echo "   export DBS_CLIENT_CONFIG=$DBS_CLIENT_ROOT/lib/Clients/Python/DBSAPI/dbs.config"; 
 echo "else";
 echo "   export DBS_CLIENT_CONFIG=$DBS_CLIENT_ROOT/lib/DBSAPI/dbs.config"; 
 echo "fi";
 echo "export DLS_PHEDEX_ENDPOINT=https://cmsweb.cern.ch/phedex/datasvc/xml/prod";
) > %{i}/etc/profile.d/dependencies-setup.sh
                                                                                                     
(echo "#!/bin/tcsh"; \
 echo "source $PYTHON_ROOT/etc/profile.d/init.csh"; \
 echo "source $PY2_PYXML_ROOT/etc/profile.d/init.csh"; \
 echo "source $DBS_CLIENT_ROOT/etc/profile.d/init.csh"; 
 echo "if [ -f $DBS_CLIENT_ROOT/lib/Clients/Python/DBSAPI/dbs.config ]; then";
 echo "   setenv DBS_CLIENT_CONFIG $DBS_CLIENT_ROOT/lib/Clients/Python/DBSAPI/dbs.config"; 
 echo "else";
 echo "   setenv DBS_CLIENT_CONFIG $DBS_CLIENT_ROOT/lib/DBSAPI/dbs.config"; 
 echo "fi";
 echo "setenv DLS_PHEDEX_ENDPOINT https://cmsweb.cern.ch/phedex/datasvc/xml/prod";
) > %{i}/etc/profile.d/dependencies-setup.csh
                                                                                                     
%post
%{relocateConfig}etc/profile.d/dependencies-setup.sh
%{relocateConfig}etc/profile.d/dependencies-setup.csh

