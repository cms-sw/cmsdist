### RPM external p5-dbd-oracle 1.23
## INITENV +PATH PERL5LIB %i/lib/site_perl/%perlversion
## BUILDIF case $(uname):$(uname -m) in Linux:i*86 ) true ;; Linux:x86_64 ) true ;;  Linux:ppc64 ) false ;; Darwin:* ) false ;; * ) false ;; esac
%define perlversion %(perl -e 'printf "%%vd", $^V')
%define perlarch %(perl -MConfig -e 'print $Config{archname}')
%define downloadn DBD-Oracle
%define closingbrace )
%define online %(case %cmsplatf in *onl_*_*%closingbrace echo true;; *%closingbrace echo false;; esac)

%if "%online" != "true"
Requires: oracle
Requires: p5-dbi
%else
Requires: onlinesystemtools
Provides: perl(DBI)
%endif

Source0: http://mirror.switch.ch/ftp/mirror/CPAN/authors/id/P/PY/PYTHIAN/%downloadn-%{realversion}.tar.gz

Provides: perl(Tk) perl(Tk::Balloon) perl(Tk::ErrorDialog) perl(Tk::FileSelect) perl(Tk::Pod) perl(Tk::ROText) 

%prep
%setup -T -b 0 -n %{downloadn}-%{realversion}

%build
%ifos darwin
perl -p -i -e 's/NMEDIT = nmedit/NMEDIT = true/' Makefile.PL
%endif

perl Makefile.PL PREFIX=%i LIB=%i/lib/site_perl/%perlversion -l -m $ORACLE_HOME/demo/demo.mk -h $ORACLE_HOME/include
make
# bla bla
