### RPM external p5-dbd-oracle 1.23
## INITENV +PATH PERL5LIB %i/lib/perl5
## BUILDIF case $(uname):$(uname -m) in Linux:i*86 | Linux:x86_64 | Darwin:* ) true ;; * ) false ;; esac
# Dummy comment: forcing the compiling for SLC6
%define downloadn DBD-Oracle
%define online %(case %cmsplatf in (*onl_*_*) echo true;; (*) echo false;; esac)

%if "%online" != "true"
Requires: oracle
Requires: p5-dbi
%else
Requires: onlinesystemtools
Provides: perl(DBI)
%endif

Source0: http://mirror.switch.ch/ftp/mirror/CPAN/authors/id/P/PY/PYTHIAN/%downloadn-%{realversion}.tar.gz
Requires: p5-extutils-makemaker
Provides: perl(Tk) perl(Tk::Balloon) perl(Tk::ErrorDialog) perl(Tk::FileSelect) perl(Tk::Pod) perl(Tk::ROText) 

%prep
%setup -T -b 0 -n %{downloadn}-%{realversion}

%build
%ifos darwin
perl -p -i -e 's/NMEDIT = nmedit/NMEDIT = true/' Makefile.PL
%endif

perl Makefile.PL INSTALL_BASE=%i -l -m $ORACLE_HOME/demo/demo.mk -h $ORACLE_HOME/include
make %{makeprocesses}

%define drop_files %i/man
