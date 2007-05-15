### RPM external p5-xml-parser 2.34
## INITENV +PATH PERL5LIB %i/lib/site_perl/%perlversion
%define perlversion %(perl -e 'printf "%%vd", $^V')
%define perlarch %(perl -MConfig -e 'print $Config{archname}')
%define downloadn XML-Parser
Requires: expat
Source: http://mirror.switch.ch/ftp/mirror/CPAN/authors/id/M/MS/MSERGEANT/%{downloadn}-%{v}.tar.gz
%prep 
%setup -n %downloadn-%v
%build

perl Makefile.PL PREFIX=%i LIB=%i/lib/site_perl/%perlversion \
                 EXPATLIBPATH=$EXPAT_ROOT/lib \
                 EXPATINCPATH=$EXPAT_ROOT/include
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
            perl Makefile.PL PREFIX=%i LIB=%i/lib/site_perl/%perlversion \
                             EXPATLIBPATH=$EXPAT_ROOT/lib64 \
                             EXPATINCPATH=$EXPAT_ROOT/include
            make
        fi;;
    *)
    ;;
esac

%install
make install
