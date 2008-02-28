### RPM external mod_python 3.2.10
# See http://www.modpython.org/live/current/doc-html/installation.html

Requires:  apache2 python

Source0: http://apache.mirror.testserver.li/httpd/modpython/mod_python-%realversion.tgz

%prep
%setup -n mod_python-%realversion

./configure --with-python=$PYTHON_ROOT/bin/python --with-apxs=$APACHE2_ROOT/bin/apxs --with-max-locks=32

%build
make

%install
make install

mkdir -p %i/conf
cat << \EOF > %i/conf/mod_python.conf
LoadModule python_module %i/modules/mod_python.so
# Additional configuration bits go here.
EOF

# By default mod_python.so and is moved to the
# $APACHE2_ROOT/modules directory, which
# is bad for us handling multiple versions in a rpm.
mkdir -p %i/modules
mv $APACHE2_ROOT/modules/mod_python.so %i/modules

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
