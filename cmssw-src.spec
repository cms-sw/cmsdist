### RPM cms cmssw-src CMSSW_6_2_X
%define cmsrepo         cvs://:pserver:anonymous@cmscvs.cern.ch:2401/local/reps/CMSSW?passwd=AA_:yZZ3e
%define srctree		src

Source: cmstc://?tag=&module=CMSSW&export=src&output=/src.tar.gz
%prep
%build
%install
# bla bla
