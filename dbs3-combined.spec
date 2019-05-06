### RPM cms dbs3-combined 3.8.1

# This is a fake spec whose only job is to build and upload 
# dbs3 and dbs3-client in one go

# To use cmsweb deployment scripts pystack and frontend are requirements
# to display their version using apt-cache depends cms+dbs3-combined+<version> 

#Requires: dbs3 dbs3-client dbs3-migration dbs3-lifecycle
Requires: dbs3 dbs3-migration dbs3-client

%prep
%build
%install
