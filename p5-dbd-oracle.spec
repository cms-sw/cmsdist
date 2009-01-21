### RPM external p5-dbd-oracle 1.17
## INITENV +PATH PERL5LIB %i/lib/site_perl/%perlversion

%define perlversion %(perl -e 'printf "%%vd", $^V')
%define perlarch %(perl -MConfig -e 'print $Config{archname}')
%define downloadn DBD-Oracle

%if "%cmsplatf" != "slc4onl_ia32_gcc346"
Requires: p5-dbi oracle
%define oraclesdksrc none
%else
# we still need oracle sdk makefiles:
%define oraclesdksrc http://cmsrep.cern.ch/cmssw/oracle-mirror/slc4_ia32/10.2.0.3/sdk.zip
%endif

Source0: http://mirror.switch.ch/ftp/mirror/CPAN/authors/id/P/PY/PYTHIAN/%downloadn-%{realversion}.tar.gz
Source1: %oraclesdksrc

Provides: perl(Tk) perl(Tk::Balloon) perl(Tk::ErrorDialog) perl(Tk::FileSelect) perl(Tk::Pod) perl(Tk::ROText)

%prep
%setup -T -b 0 -n %{downloadn}-%{realversion}

%if "%cmsplatf" == "slc4onl_ia32_gcc346"
rm -rf instantclient_*
yes | unzip %_sourcedir/sdk.zip
%endif

%build
%ifos darwin
perl -p -i -e 's/NMEDIT = nmedit/NMEDIT = true/' Makefile.PL
%endif

%if "%cmsplatf" != "slc4onl_ia32_gcc346"
perl Makefile.PL PREFIX=%i LIB=%i/lib/site_perl/%perlversion -l -m $ORACLE_HOME/demo/demo.mk
%else
export ORACLE_HOME="/opt/xdaq"
perl Makefile.PL PREFIX=%i LIB=%i/lib/site_perl/%perlversion -l -m instantclient_10_2/demo/demo.mk
%endif
make
