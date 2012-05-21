### RPM test testdownload 1.0
## NOCOMPILER
Source0: http://switch.dl.sourceforge.net/sourceforge/yui/yui_2.3.1.zip
Source1: cvs://:pserver:anonymous@cmssw.cvs.cern.ch:2401/local/reps/CMSSW?passwd=AA_:yZZ3e&module=CMSDIST&export=CMSDIST&&tag=-rHEAD&output=/CMSDIST.tar.gz
Source2: svn://root.cern.ch/svn/root/trunk?scheme=https&module=root&output=/root.tgz
Source3: cmstc://?tag=CMSSW_6_0_X_2012-05-21-0200&module=CMSSW&export=src&output=/src.tar.gz

%prep
sha1sum %_sourcedir/yui_2.3.1.zip
sha1sum %_sourcedir/root.tgz
sha1sum %_sourcedir/CMSDIST.tar.gz
sha1sum %_sourcedir/src.tar.gz
%build
%install
