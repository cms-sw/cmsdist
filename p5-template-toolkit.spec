### RPM external p5-template-toolkit 2.15-CMS19
## INITENV +PATH PATH %{i}/bin
## INITENV +PATH PERL5LIB %i/lib/site_perl/%perlversion
%define perl /usr/bin/env perl
%if "%(echo %cmsplatf | cut -f1 -d_ | sed -e 's|\([A-Za-z]*\)[0-9]*|\1|')" == "osx"
%define perl /usr/bin/perl
%endif

%define perlversion %(%perl -e 'printf "%%vd", $^V')
%define perlarch %(%perl -MConfig -e 'print $Config{archname}')
%define downloadn Template-Toolkit

Provides: perl(AppConfig)
Provides: perl(GD)
Provides: perl(GD::Graph::area)
Provides: perl(GD::Graph::bars)
Provides: perl(GD::Graph::bars3d)
Provides: perl(GD::Graph::lines)
Provides: perl(GD::Graph::lines3d)
Provides: perl(GD::Graph::linespoints)
Provides: perl(GD::Graph::mixed)
Provides: perl(GD::Graph::pie)
Provides: perl(GD::Graph::pie3d)
Provides: perl(GD::Graph::points)
Provides: perl(GD::Text)
Provides: perl(GD::Text::Align)
Provides: perl(GD::Text::Wrap)
Provides: perl(Pod::POM) 
Provides: perl(Text::Autoformat)
Provides: perl(XML::DOM)
Provides: perl(XML::RSS)
Provides: perl(XML::Simple)
Provides: perl(XML::XPath)

Source: http://www.cpan.org/modules/by-module/Template/%downloadn-%{realversion}.tar.gz

%prep
%setup -n %{downloadn}-%{realversion}
%build
%perl Makefile.PL PREFIX=%i LIB=%i/lib/site_perl/%perlversion \
		 TT_LIB=%{i}/lib/site_perl/%perlversion \
                 TT_PREFIX=%{i} \
                 TT_ACCEPT=y \
                 TT_DOCS=n \
                 TT_EXAMPLES=n \
                 TT_SPLASH=n \
                 TT_DBI=n
%perl -p -i -e 's!install :: (.*) tt2_splash!install :: $1!' Makefile
make
%perl -p -i -e 's|^#!.*perl(.*)|#!%perl$1|' blib/script/tpage
%perl -p -i -e 's|^#!.*perl(.*)|#!%perl$1|' blib/script/ttree
case %{cmsos} in
    slc4_ia32)
    if ldd /usr/bin/gcc | grep -q /lib64/
    then
        make install
        mv %i/lib/site_perl/%perlversion/x86_64-linux-thread-multi  %i/lib/site_perl/%perlversion/i386-linux-thread-multi
        make clean
        export PATH=/usr/bin/:$PATH
        export GCC_EXEC_PREFIX=/usr/lib/gcc/
        %perl Makefile.PL PREFIX=%i LIB=%i/lib/site_perl/%perlversion \
                         TT_LIB=%{i}/lib/site_perl/%perlversion \
                         TT_PREFIX=%{i} \
                         TT_ACCEPT=y \
                         TT_DOCS=n \
                         TT_EXAMPLES=n \
                         TT_SPLASH=n \
                         TT_DBI=n
        %perl -p -i -e 's!install :: (.*) tt2_splash!install :: $1!' Makefile
        make
        %perl -p -i -e 's|^#!.*perl(.*)|#!%perl$1|' blib/script/tpage
        %perl -p -i -e 's|^#!.*perl(.*)|#!%perl$1|' blib/script/ttree
    fi;;
    *)
    ;;
    esac

%install
make install
