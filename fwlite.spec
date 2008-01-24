### RPM cms fwlite CMSSW_1_6_8_FWLITE-root51800
## IMPORT configurations 
Provides: /bin/zsh
Requires: fwlite-tool-conf 
%define cmssw_release 	%(perl -e '$_="%v"; s/_FWLITE-root51800//; print;')
%define toolconf        ${FWLITE_TOOL_CONF_ROOT}/configurations/tools-STANDALONE.conf

#Defines for file containing list of packages for checkout and build:
%define buildsetrepo 	CMSDIST
%define buildsetfile 	fwlite_build_set.file
%define buildsetvers	buildset_V3_3

# Define list of external tools to be selected in scram configuration.
# Any changes must be propagated in fwlite-tool-conf.spec:
%define externals "cxxcompiler ccompiler clhep sockets boost boost_filesystem boost_python boost_regex boost_program_options root rootcintex rootrflx rootcore rootmath gccxml python elementtree sigcpp hepmc gsl bz2lib pcre zlib dcap libjpg openssl expat"

%define buildtarget     release-build

# Skip library load and symbol checks to avoid dependency on seal:
%define nolibchecks	on

# Switch off building tests:
%define patchsrc3 perl -p -i -e ' s!(<ClassPath.*test\\+test>)!#$1!;' config/BuildFile

# Additional source patches named patchsrc4, patchsrc5 can be defined here.
%define patchsrc4 perl -p -i -e '/<lib name=Tree>/ && print "<lib name=Net>\n<lib name=RIO>\n";' SCRAMToolBox/General/ROOTCore

## IMPORT cms-scram-build
## IMPORT partial-build
## IMPORT scramv1-build
