### RPM external mod_perl2 2.0.7
## INITENV +PATH PERL5LIB %i/lib/perl5
# See http://perl.apache.org/docs/2.0/user/install/install.html
Source0: http://perl.apache.org/dist/mod_perl-%realversion.tar.gz

# Requires apache2
# Requires p5-cgi -- system SLC4 system CGI.pm is broken for mod_perl2
Requires: apache2 p5-cgi p5-extutils-makemaker p5-linux-pid p5-test-harness p5-test-simple

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
perl Makefile.PL INSTALL_BASE=%i MP_APXS=$APACHE2_ROOT/bin/apxs MP_AP_DESTDIR=%i
make %makeprocesses

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
find %i/lib/perl5 -name '*PHP*.pm' -exec rm -f {} \;

# Generate dependencies-setup.{sh,csh} so init.{sh,csh} picks full environment.
mkdir -p %i/etc/profile.d
: > %i/etc/profile.d/dependencies-setup.sh
: > %i/etc/profile.d/dependencies-setup.csh
for tool in $(echo %{requiredtools} | sed -e's|\s+| |;s|^\s+||'); do
  root=$(echo $tool | tr a-z- A-Z_)_ROOT; eval r=\$$root
  if [ X"$r" != X ] && [ -r "$r/etc/profile.d/init.sh" ]; then
    echo "test X\$$root != X || . $r/etc/profile.d/init.sh" >> %i/etc/profile.d/dependencies-setup.sh
    echo "test X\$?$root = X1 || source $r/etc/profile.d/init.csh" >> %i/etc/profile.d/dependencies-setup.csh
  fi
done

# Strip libraries, we are not going to debug them.
%define strip_files %i/{lib,modules}

# Look up documentation online.
%define drop_files %i/man

%post
%{relocateConfig}conf/mod_perl2.conf
%{relocateConfig}lib/perl5/*/Apache2/BuildConfig.pm
%{relocateConfig}etc/profile.d/dependencies-setup.*sh
