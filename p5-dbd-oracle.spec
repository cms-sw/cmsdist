### RPM external p5-dbd-oracle 1.17-CMS19
## INITENV +PATH PERL5LIB %i/lib/site_perl/%perlversion
%define perlversion %(perl -e 'printf "%%vd", $^V')
%define perlarch %(perl -MConfig -e 'print $Config{archname}')
%define downloadn DBD-Oracle
Source: http://mirror.switch.ch/ftp/mirror/CPAN/authors/id/P/PY/PYTHIAN/%downloadn-%{realversion}.tar.gz

Requires: p5-dbi oracle
Provides: perl(Tk) perl(Tk::Balloon) perl(Tk::ErrorDialog) perl(Tk::FileSelect) perl(Tk::Pod) perl(Tk::ROText)

%prep
%setup -n %{downloadn}-%{realversion}

%build
patch Makefile.PL << \EOF
diff Makefile.PL.orig Makefile.PL
1407a1408
>        "$OH/include", # Tim Barrass, hacked for OIC install from zips
EOF
%ifos darwin
perl -p -i -e 's/NMEDIT = nmedit/NMEDIT = true/' Makefile.PL
%endif

perl Makefile.PL PREFIX=%i LIB=%i/lib/site_perl/%perlversion -l -m $ORACLE_HOME/demo/demo.mk
make
#
