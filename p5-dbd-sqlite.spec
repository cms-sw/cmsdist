### RPM external p5-dbd-sqlite 1.31
## INITENV +PATH PERL5LIB %i/lib/site_perl/%perlversion
%define perlversion %(perl -e 'printf "%%vd", $^V')
%define perlarch %(perl -MConfig -e 'print $Config{archname}')
%define downloadn DBD-SQLite
%define online %(case %cmsplatf in (*onl_*_*) echo true;; (*) echo false;; esac)
Source: http://search.cpan.org/CPAN/authors/id/A/AD/ADAMK/%downloadn-%realversion.tar.gz
Requires: sqlite
%if "%online" != "true"
Requires: p5-dbi
%else
Provides: perl(DBI)
%endif

%prep
%setup -n %{downloadn}-%{realversion}

%build
perl Makefile.PL PREFIX=%i LIB=%i/lib/site_perl/%perlversion SQLITE_LOCATION=$SQLITE_ROOT
make
