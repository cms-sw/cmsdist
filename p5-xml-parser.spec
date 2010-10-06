### RPM external p5-xml-parser 2.36
## INITENV +PATH PERL5LIB %i/lib/site_perl/%perlversion

%define perl /usr/bin/env perl
%if "%(echo %cmsplatf | cut -f1 -d_ | sed -e 's|\([A-Za-z]*\)[0-9]*|\1|')" == "osx" 
%define perl /usr/bin/perl
%endif

%define perlversion %(%perl -e 'printf "%%vd", $^V')
%define perlarch %(%perl -MConfig -e 'print $Config{archname}')
%define downloadn XML-Parser
%define expatversion 2.0.0
Source0: http://mirror.switch.ch/ftp/mirror/CPAN/authors/id/M/MS/MSERGEANT/%{downloadn}-%{realversion}.tar.gz
Source1: http://dl.sourceforge.net/sourceforge/expat/expat-%expatversion.tar.gz
Provides: libc.so.6()(64bit)
Provides: libc.so.6(GLIBC_2.2.5)(64bit)  

%prep 
%setup -T -b 0 -n %{downloadn}-%{realversion}
%setup -D -T -b 1 -n expat-%expatversion
%build
# We statically compile expat so that the perl module itself,
# and hence scram, do not depend on the expat rpm.
# This way we can change the expat version in CMSSW/externals
# without having to rebuild scram. 
which gcc
rm -rf %_builddir/tmp
cd ../expat-%expatversion
mkdir -p %_builddir/tmp
./configure --prefix=%_builddir/tmp --disable-shared --enable-static --with-pic
make clean
make 
make install
cd ../%{downloadn}-%{realversion}

%perl Makefile.PL PREFIX=%i LIB=%i/lib/site_perl/%perlversion \
                 EXPATLIBPATH=%_builddir/tmp/lib \
                 EXPATINCPATH=%_builddir/tmp/include
make
make install

%install
