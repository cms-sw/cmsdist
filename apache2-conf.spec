### RPM cms apache2-conf 1.0
# Configuration for additional apache2 modules
Source: none
Requires:  mod_perl2 mod_python apache2

%prep
%build
%install
mkdir -p %i/conf %i/bin

# FIXME: make sure that mod_perl2.conf/mod_python.conf are actually called that way. 
# FIXME: autogenerate from Requires.
cat << \EOF > %i/conf/apache2.conf
Include @APACHE2_ROOT@/conf/httpd.conf
Include @MOD_PERL2_ROOT@/conf/mod_perl2.conf
Include @MOD_PYTHON_ROOT@/conf/mod_python.conf
# Additional configuration bits go here.
EOF

cat << \EOF > %i/bin/httpd
#!/bin/sh
@APACHE2_ROOT@/bin/httpd -f %i/conf/apache2.conf ${1+"$@"}
EOF

perl -p -i -e "s|\@APACHE2_ROOT\@|$APACHE2_ROOT|g;
               s|\@MOD_PERL2_ROOT\@|$MOD_PERL2_ROOT|g;
               s|\@MOD_PYTHON_ROOT\@|$MOD_PYTHON_ROOT|g;" %i/conf/apache2.conf %i/bin/httpd

chmod +x %i/bin/httpd

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
%{relocateConfig}bin/httpd
%{relocateConfig}conf/apache2.conf
