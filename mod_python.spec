### RPM external mod_python 3.2.10
## INITENV +PATH PYTHONPATH %i/lib/python`echo $PYTHON_VERSION | cut -d. -f 1,2`/site-packages

# See http://www.modpython.org/live/current/doc-html/installation.html

Requires:  apache2 python
Source0: http://mirror.switch.ch/mirror/apache/dist/httpd/modpython/mod_python-%realversion.tgz

%prep
%setup -n mod_python-%realversion

# note: --prefix and --exec-prefix mean nothing to this package...
./configure --with-python=$PYTHON_ROOT/bin/python --with-apxs=$APACHE2_ROOT/bin/apxs --with-max-locks=32

%build
make

%install
# note:  need undocumented DESTDIR to move the install area
DESTDIR=%i make install

mkdir -p %i/conf
cat << \EOF > %i/conf/mod_python.conf
LoadModule python_module %i/modules/mod_python.so
# Additional configuration bits go here.
EOF

# By default mod_perl.so and include/ directory is moved to the
# $APACHE2_ROOT/modules and $APACHE2_ROOT/include, respectively, which
# is bad for us handling multiple versions in a rpm. With
# --with-apxs set this changes to %i/$APACHE2_ROOT, which will be a
# long directory path hardcoded at build time.  Therefore, we have to
# move these resources back to a sane location and clean up.  The same
# goes for the python libraries.
mv %i/$APACHE2_ROOT/* %i
mv %i/$PYTHON_ROOT/* %i
rm -r %i/build

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
%{relocateConfig}conf/mod_python.conf
%{relocateConfig}etc/profile.d/dependencies-setup.sh
%{relocateConfig}etc/profile.d/dependencies-setup.csh
