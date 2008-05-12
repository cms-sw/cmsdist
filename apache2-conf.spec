### RPM cms apache2-conf 1.4
# Configuration for additional apache2 modules

# Version of this RPM is defined by CVS revision number of the configuration file
%define confURL http://cmssw.cvs.cern.ch/cgi-bin/cmssw.cgi/COMP/WEBTOOLS/Configuration/apache2.conf?revision=%v
Source: none
Requires:  mod_perl2 mod_python apache2

%prep
%build
%install

# Make directory for various resources of this package
mkdir -p %i/conf %i/bin %i/htdocs %i/logs %i/apps.d %i/var %i/startenv.d

wget -O %i/conf/apache2.conf %confURL

# Make a script to start apache with our environment and configuration file

cat << \EOF > %i/bin/httpd
#!/bin/sh
for file in `find %i/startenv.d -type f`; do
  source $file
done
 
@APACHE2_ROOT@/bin/httpd -f %i/conf/apache2.conf ${1+"$@"}
EOF

chmod +x %i/bin/httpd

# Switch template variables in the configuration file and startup script

export SERVER_ROOT=%i
perl -p -i -e "s|\@SERVER_ROOT\@|$SERVER_ROOT|g;
               s|\@APACHE2_ROOT\@|$APACHE2_ROOT|g;
               s|\@MOD_PERL2_ROOT\@|$MOD_PERL2_ROOT|g;
               s|\@MOD_PYTHON_ROOT\@|$MOD_PYTHON_ROOT|g;" %i/conf/apache2.conf %i/bin/httpd

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

# Copy the dependencies to our environment directory

cp %i/etc/profile.d/dependencies-setup.sh %i/startenv.d/apache2.sh

%post
%{relocateConfig}bin/httpd
%{relocateConfig}conf/apache2.conf
%{relocateConfig}startenv.d/apache2.sh
%{relocateConfig}etc/profile.d/dependencies-setup.sh
%{relocateConfig}etc/profile.d/dependencies-setup.csh
