### RPM external mod_perl2 2.0.3
## INITENV +PATH PERL5LIB %i/lib/site_perl/%perlversion

%define perlversion %(perl -e 'printf "%%vd", $^V')
%define perlarch %(perl -MConfig -e 'print $Config{archname}')

# See http://perl.apache.org/docs/2.0/user/install/install.html

Source0: http://perl.apache.org/dist/mod_perl-%realversion.tar.gz

# Only require apache2 since perl is seeded from the system.
Requires: apache2

# Doesn't actually provide these, but supposedly not needed for
# non-developers of mod_perl
Provides: perl(Apache2::FunctionTable)
Provides: perl(Apache2::StructureTable)
Provides: perl(Apache::TestConfigParse)
Provides: perl(Apache::TestConfigPerl)
Provides: perl(BSD::Resource)
Provides: perl(Data::Flow)
Provides: perl(Module::Build)
 

%prep
%setup -n mod_perl-%realversion

%build
perl Makefile.PL PREFIX=%i LIB=%i/lib/site_perl/%perlversion MP_APXS=$APACHE2_ROOT/bin/apxs MP_AP_DESTDIR=%i
make

%install
make install

mkdir -p %i/conf
cat << \EOF > %i/conf/mod_perl2.conf
LoadModule perl_module %i/modules/mod_perl.so
# Additional configuration bits go here.
EOF

# By default mod_perl.so and include/ directory is moved to the
# $APACHE2_ROOT/modules and $APACHE2_ROOT/include, respectively, which
# is bad for us handling multiple versions in a rpm. With
# MP_AP_DESTDIR=%i this changes to %i/$APACHE2_ROOT, which will be a
# long directory path hardcoded at build time.  Therefore, we have to
# move these resources back to a sane location and clean up.
mv %i/$APACHE2_ROOT/* %i
rm -r %i/$(echo $APACHE2_ROOT | sed 's|^/||' | cut -d/ -f1)

# Generates the dependencies-setup.{sh,csh} files so that
# sourcing init.{sh,csh} picks up also the environment of 
# dependencies.

rm -rf %i/etc/profile.d
mkdir -p %i/etc/profile.d
echo '#!/bin/sh' > %{i}/etc/profile.d/dependencies-setup.sh
echo '#!/bin/tcsh' > %{i}/etc/profile.d/dependencies-setup.csh
echo requiredtools `echo %{requiredtools} | sed -e's|\s+| |;s|^\s+||'`
for tool in `echo %{requiredtools} | sed -e's|\s+| |;s|^\s+||'`
do
    case X$tool in
        Xdistcc|Xccache )
        ;;
        * )
            toolcap=`echo $tool | tr a-z- A-Z_`
            eval echo ". $`echo ${toolcap}_ROOT`/etc/profile.d/init.sh" >> %{i}/etc/profile.d/dependencies-setup.sh
            eval echo "source $`echo ${toolcap}_ROOT`/etc/profile.d/init.csh" >> %{i}/etc/profile.d/dependencies-setup.csh
        ;;
    esac
done

perl -p -i -e 's|\. /etc/profile\.d/init\.sh||' %{i}/etc/profile.d/dependencies-setup.sh
perl -p -i -e 's|source /etc/profile\.d/init\.csh||' %{i}/etc/profile.d/dependencies-setup.csh


%post
%{relocateConfig}conf/mod_perl2.conf
%{relocateConfig}etc/profile.d/dependencies-setup.sh
%{relocateConfig}etc/profile.d/dependencies-setup.csh
