### RPM test testdownload 1.0
Source0: http://www.lua.org/ftp/lua-5.1.4.tar.gz
Source1: cvs://:pserver:anonymous@cmssw.cvs.cern.ch:/local/reps/CMSSW?passwd=AA_:yZZ3e&module=PKGTOOLS&export=PKGTOOLS&tag=-rHEAD&output=/PKGTOOLS.tar.gz
Source2: svn://cvs2svn.tigris.org/svn/cvs2svn/trunk?scheme=http&revision=5419&module=cvs2git-5419&output=/cvs2git-5419.tgz
Source3: git://github.com/cms-sw/pkgtools.git?obj=V00-21-XX/HEAD&export=pkgtools&filter=*/docs/*&output=/pkgtools-docs.tgz
Source4: git://github.com/cms-sw/pkgtools.git?obj=V00-21-XX/HEAD&export=pkgtools&output=/pkgtools.tgz
#Source3: cmstc://?tag=CMSSW_1_8_0_pre4&module=CMSSW&export=src&output=/src.tar.gz

%prep
%build
%install
# bla bla
