### RPM cms rpm-verify RPMVERIFY_0_1
##%define downloadn %(echo %n | cut -f1 -d-)
Source: cvs://:pserver:anonymous@cmscvs.cern.ch:2401/cvs_server/repositories/CMSSW?passwd=AA_:yZZ3e&module=UserCode/DiegoGomes&export=%{n}&&tag=-r%{v}&output=/%{n}.sh
##Requires: rpm 

%prep
rm -rf %{i}
mkdir -p %{i}
cp %{_sourcedir}/rpm-verify.sh %{i}/

%build

%install
chmod 755 %i/rpm-verify.sh

%post

%files
%i/rpm-verify.sh

