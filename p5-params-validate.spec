### RPM external p5-params-validate 0.91
## INITENV +PATH PERL5LIB %i/lib/site_perl/%perlversion
%define perlversion %(perl -e 'printf "%%vd", $^V')
%define perlarch %(perl -MConfig -e 'print $Config{archname}')
%define downloadn Params-Validate

# There where some problems using the parameterized version
# with cmsbuild so I substituted the hard values.
# the commented out lines are from the original (fvlingen@caltech.edu)
#Source: http://search.cpan.org/CPAN/authors/id/D/DR/DROLSKY/%{downloadn}-%{v}.tar.gz
Source: http://search.cpan.org/CPAN/authors/id/D/DR/DROLSKY/Params-Validate-0.91.tar.gz

%prep
#%setup -n %downloadn-%v
%setup -n Params-Validate-0.91
%build
LC_ALL=C; export LC_ALL
perl Makefile.PL PREFIX=%i LIB=%i/lib/site_perl/%perlversion
make
#
