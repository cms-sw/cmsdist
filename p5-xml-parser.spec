### RPM external p5-xml-parser 2.41
## INITENV +PATH PERL5LIB %i/lib/perl5
# Dummy comment: forcing the compiling for SLC6
%define downloadn XML-Parser
%define expatversion 2.0.0
Source0: http://search.cpan.org/CPAN/authors/id/T/TO/TODDR/%{downloadn}-%{realversion}.tar.gz
Source1: http://downloads.sourceforge.net/expat/expat/%expatversion/expat-%expatversion.tar.gz
Requires: p5-extutils-makemaker
Provides: libc.so.6()(64bit)
Provides: libc.so.6(GLIBC_2.2.5)(64bit)  

%prep
%setup -T -b 1 -n expat-%expatversion
%setup -D -T -b 0 -n %{downloadn}-%{realversion}

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
make %{makeprocesses}
make install

cd ../%{downloadn}-%{realversion}
perl Makefile.PL INSTALL_BASE=%i EXPATLIBPATH=%_builddir/tmp/lib EXPATINCPATH=%_builddir/tmp/include
make %{makeprocesses}

%install
make install
find %i -name LWPExternEnt.pl -exec rm -f {} \;
%define drop_files %i/man
