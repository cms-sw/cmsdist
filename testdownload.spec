### RPM test testdownload 1.0
Source0: http://switch.dl.sourceforge.net/sourceforge/yui/yui_2.3.1.zip
Source1: cvs://:pserver:anonymous@cmscvs.cern.ch:2401/cvs_server/repositories/CMSSW?passwd=AA_:yZZ3e&module=PRODCOMMON&export=PRODCOMMON&&tag=-rHEAD&output=/PRODCOMMON.tar.gz
Source2: svn://root.cern.ch/svn/root/trunk?scheme=https&module=root&output=/root.tgz
#Source3: cmstc://?tag=CMSSW_1_8_0_pre4&module=CMSSW&export=src&output=/src.tar.gz

%pre
%build
%install
