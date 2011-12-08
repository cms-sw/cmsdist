### RPM test download-test 1.0
## NOCOMPILER

%define dummy foo=%(date +%Y%m%d%H%M%s)
Source0: ftp://ftp.coin3d.org/pub/coin/src/all/SoQt-1.5.0.tar.gz
Source1: svn://root.cern.ch/svn/root/trunk?scheme=http&strategy=export&module=root-HEAD&tag=42440&%dummy&output=/root-HEAD.tgz
Source2: svn+http://root.cern.ch/svn/root/trunk?strategy=export&module=root-HEAD&tag=42440&output=/root-HEAD2.tgz
Source3: svn+https://root.cern.ch/svn/root/trunk?strategy=export&module=root-HEAD&tag=42440&%dummy&output=/root-HEAD3.tgz
Source4: git://github.com/ktf/apt-rpm.git?%dummy&output=/apt-rpm.tgz
Source5: git+https://github.com/ktf/apt-rpm.git?%dummy&output=/apt-rpm.tgz
Source6: http://www.hepforge.org/archive/professor/professor-1.3.1.tar.gz?%dummy&output=/professor.tar.gz
Source7: cvs://:pserver:anonymous@cmscvs.cern.ch:2401/cvs_server/repositories/CMSSW?passwd=AA_:yZZ3e&module=PHEDEX&export=PHEDEX&&tag=-rPHEDEX_3_3_2&%dummy&output=/PHEDEX.tar.gz
Source8: cmstc://?tag=CMSSW_5_0_0_pre7&module=CMSSW&%dummy&export=src&output=/src.tar.gz

%prep
# This is obviously only valid for my account, since the owner in some cases changes.
[ X668b44bbe266f039f8b10ee250fe9a7a = "X`md5sum %_sourcedir/PHEDEX.tar.gz | cut -f1 -d\ `" ]
[ X9f1e582373d66f556b1db113a93ac68e = "X`md5sum %_sourcedir/SoQt-1.5.0.tar.gz | cut -f1 -d\ `" ]
[ Xb87fc45ad93bcbbe9df2bbd902f3affc = "X`md5sum %_sourcedir/apt-rpm.tgz | cut -f1 -d\ `" ]
[ X959374e7ca69d4456a260f7c8e7156a4 = "X`md5sum %_sourcedir/professor.tar.gz | cut -f1 -d\ `" ]
[ Xfa59db1bd440a5b54c04f0b5f5155017 = "X`md5sum %_sourcedir/root-HEAD.tgz | cut -f1 -d\ `" ]
[ Xb341461732a7bc63d3988b55e57e3763 = "X`md5sum %_sourcedir/root-HEAD2.tgz | cut -f1 -d\ `" ]
[ X04128c80c550c1a183207e4932ff85a3 = "X`md5sum %_sourcedir/root-HEAD3.tgz | cut -f1 -d\ `" ]
# This is not even true, because the timestamp changes.
#[ X97cb55e7e3df40819778047b51a3bf0f = "X`md5sum %_sourcedir/src.tar.gz | cut -f1 -d\ `" ]
%build
%install
