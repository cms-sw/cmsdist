### RPM cms das-client 0.9.7
## NOCOMPILER
%define svnserver svn://svn.cern.ch/reps/CMSDMWM
Source0: %svnserver/DAS/tags/%{realversion}/src/python/DAS/tools/?scheme=svn+ssh&strategy=export&module=DAS&output=/das-client.tar.gz

%prep
%setup -D -T -b 0 -n DAS

%build
%install
mkdir -p %{i}/bin
cp das_client.py %{i}/bin/
