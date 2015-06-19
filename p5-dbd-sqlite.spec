### RPM external p5-dbd-sqlite 1.31
## INITENV +PATH PERL5LIB %i/lib/perl5
%define downloadn DBD-SQLite
%define online %(case %cmsplatf in (*onl_*_*) echo true;; (*) echo false;; esac)
Source: http://search.cpan.org/CPAN/authors/id/A/AD/ADAMK/%downloadn-%realversion.tar.gz
Requires: sqlite p5-extutils-makemaker
%if "%online" != "true"
Requires: p5-dbi
%else
Provides: perl(DBI)
%endif

%prep
%setup -n %{downloadn}-%{realversion}

%build
perl Makefile.PL INSTALL_BASE=%i SQLITE_LOCATION=$SQLITE_ROOT
make %{makeprocesses}

%define drop_files %i/man
