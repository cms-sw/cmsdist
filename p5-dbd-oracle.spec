### RPM external p5-dbd-oracle 1.17-CMS24
## INITENV +PATH PERL5LIB %i/lib/site_perl/%perlversion
# a comment to build from scratch increase this number 15
%define perl /usr/bin/env perl
%if "%(echo %cmsplatf | cut -f1 -d_ | sed -e 's|\([A-Za-z]*\)[0-9]*|\1|')" == "osx"
%define perl /usr/bin/perl
%endif

%define perlversion %(%perl -e 'printf "%%vd", $^V')
%define perlarch %(%perl -MConfig -e 'print $Config{archname}')
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
%perl -p -i -e 's/NMEDIT = nmedit/NMEDIT = true/' Makefile.PL
%endif

%if "%cmsplatf" != "slc4onl_ia32_gcc346"
%perl Makefile.PL PREFIX=%i LIB=%i/lib/site_perl/%perlversion -l -m $ORACLE_HOME/demo/demo.mk
%else
export ORACLE_HOME="/opt/xdaq"
%perl Makefile.PL PREFIX=%i LIB=%i/lib/site_perl/%perlversion -l -m instantclient_10_2/demo/demo.mk
%endif
make

case %{cmsos} in
    slc4_ia32)
    if ldd /usr/bin/gcc | grep -q /lib64/
    then
        make install
        mv %i/lib/site_perl/%perlversion/x86_64-linux-thread-multi  %i/lib/site_perl/%perlversion/i386-linux-thread-multi
        make clean
        export PATH=/usr/bin/:$PATH
        export GCC_EXEC_PREFIX=/usr/lib/gcc/
	ORACLE_HOME=$ORACLE_HOME/oracle64
	%perl Makefile.PL PREFIX=%i LIB=%i/lib/site_perl/%perlversion -l -m $ORACLE_HOME/demo/demo.mk
        make
        make install
     else
        make install
     fi;;
    *)
        make install
    ;;
esac

%install
