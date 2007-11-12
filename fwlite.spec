### RPM cms fwlite CMSSW_1_6_0_pre5_FWLITE
## IMPORT configurations 
Provides: /bin/zsh
Requires: fwlite-tool-conf 
%define cmssw_release 	%(perl -e '$_="%v"; s/_FWLITE//; print;')
%define toolconf        ${FWLITE_TOOL_CONF_ROOT}/configurations/tools-STANDALONE.conf

#Defines for file containing list of packages for checkout and build:
%define buildsetrepo 	CMSDIST
%define buildsetfile 	fwlite_build_set.file
%define buildsetvers	buildset_V3_0

# Define list of external tools to be selected in scram configuration.
# Any changes must be propagated in fwlite-tool-conf.spec:
%define externals "cxxcompiler ccompiler clhep sockets boost boost_filesystem rootrflx rootcore rootmath gccxml boost_python elementtree sigcpp hepmc gsl boost_regex boost_program_options boost_program_options boost_regex bz2lib pcre root rootcintex zlib glimpse"


%define prebuildtarget  gindices
%define buildtarget     release-build

# Skip library load and symbol checks to avoid dependency on seal:
%define nolibchecks	on

# Switch off building tests:
%define patchsrc3 perl -p -i -e ' s!(<ClassPath.*test\\+test>)!#$1!;' config/BuildFile

# Additional source patches named patchsrc4, patchsrc5 can be defined here.

## IMPORT cms-scram-build
## IMPORT partial-build
## IMPORT scramv1-build
