### RPM external p5-dbd-oracle 1.17-CMS18
## INITENV +PATH PERL5LIB %i/lib/site_perl/%perlversion
%define perlversion %(perl -e 'printf "%%vd", $^V')
%define perlarch %(perl -MConfig -e 'print $Config{archname}')
%define downloadn DBD-Oracle
Source0: http://mirror.switch.ch/ftp/mirror/CPAN/authors/id/P/PY/PYTHIAN/%downloadn-%{realversion}.tar.gz
# Download required makefile from oracle distribution on CMS server:
Source1: http://cmsrep.cern.ch/cms/cpt/Software/download/cms/SOURCES/external/oracle/10.2.0.3-CMS18/instantclient-sdk-linux32-10.2.0.3-20061115.zip
%define oraclesdkdir instantclient_10_2
# Requires: p5-dbi  # this comes from system
Provides: perl(Tk) perl(Tk::Balloon) perl(Tk::ErrorDialog) perl(Tk::FileSelect) perl(Tk::Pod) perl(Tk::ROText)

%prep
%setup -T -b 0 -n %{downloadn}-%{realversion}
rm -rf instantclient_*
yes | unzip %_sourcedir/*-sdk-*linux32*.zip

%build
patch Makefile.PL << \EOF
diff Makefile.PL.orig Makefile.PL
1407a1408
>        "$OH/include", # Tim Barrass, hacked for OIC install from zips
EOF
%ifos darwin
[ $(uname) = Darwin ] perl -p -i -e 's/NMEDIT = nmedit/NMEDIT = true/' Makefile.PL
%endif
export ORACLE_HOME="/opt/xdaq"
perl Makefile.PL PREFIX=%i LIB=%i/lib/site_perl/%perlversion -l -m %{oraclesdkdir}/sdk/demo/demo.mk
make
#
