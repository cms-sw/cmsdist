### RPM external couchdb 0.8.1
Source: http://mirrors.directorymix.com/apache/incubator/%n/%realversion-incubating/apache-%n-%realversion-incubating.tar.gz
Requires: gcc curl spidermonkey openssl icu4c erlang

%prep
#%setup -n %n-%{realversion}
%setup -n apache-%n-%{realversion}-incubating

%build
export PATH=$PATH:$ICU4CU_ROOT/bin:$ERLANG_ROOT/bin
./configure --prefix=%i --with-js-lib=$SPIDERMONKEY_ROOT/lib --with-js-include=$SPIDERMONKEY_ROOT/include --with-erlang=$ERLANG_ROOT/lib/erlang/usr/include
make

%install
export PATH=$PATH:$ICU4CU_ROOT/bin:$ERLANG_ROOT/bin
make install DESTDIR=$RPM_BUILD_ROOT

# Install couchdb initscript
install -D -m 755 %{SOURCE1} $RPM_BUILD_ROOT%{_initrddir}/%{name}

# Create /var/log/couchdb
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/log/couchdb

# Create /var/run/couchdb
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/run/couchdb

# Create /var/lib/couchdb
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/lib/couchdb

# Use /etc/sysconfig instead of /etc/default
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
mv $RPM_BUILD_ROOT%{_sysconfdir}/default/couchdb \
   $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/couchdb
rm -rf $RPM_BUILD_ROOT%{_sysconfdir}/default

# Modify local of couchdb.pid
#sed -i 's/\%{_localstatedir}\/run\/couchdb.pid/\%{_localstatedir}\/run\/couchdb\/couchdb.pid/g' \
#$RPM_BUILD_ROOT%{_sysconfdir}/default/couchdb
sed -i 's/\%{_localstatedir}\/run\/couchdb.pid/\%{_localstatedir}\/run\/couchdb\/couchdb.pid/g' \
$RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/couchdb

# Modify couchdb script to use env. variables rather then full path
cat $RPM_BUILD_ROOT/bin/couchdb | sed -i 's,$ICU4CU_ROOT,\\$ICU4CU_ROOT,g' \
        > $RPM_BUILD_ROOT/bin/couchdb.new
cat $RPM_BUILD_ROOT/bin/couchdb.new sed 's,$ERLANG_ROOT,\\$ERLANG_ROOT,g' \
        > $RPM_BUILD_ROOT/bin/couchdb
rm -f $RPM_BUILD_ROOT/bin/couchdb.new
   
# SCRAM ToolBox toolfile
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/%n
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=Couchdb version=%v>
<lib name=coucndb>
<client>
 <Environment name=COUCHDB_BASE default="%i"></Environment>
 <Environment name=INCLUDE default="$COUCHDB_BASE/include"></Environment>
 <Environment name=LIBDIR  default="$COUCHDB_BASE/lib"></Environment>
</client>
<Runtime name=PATH value="$COUCHDB_BASE/bin" type=path>
</Tool>
EOF_TOOLFILE

# This will generate the correct dependencies-setup.sh/dependencies-setup.csh
# using the information found in the Requires statements of the different
# specs and their dependencies.
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
%{relocateConfig}etc/scram.d/%n
%{relocateConfig}etc/profile.d/dependencies-setup.sh
%{relocateConfig}etc/profile.d/dependencies-setup.csh

