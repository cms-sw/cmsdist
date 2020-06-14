### RPM cms pystack3 2.1
Source: git://github.com/dmwm/pystack?obj=master/%{realversion}&export=pystack&output=/src.tar.gz
Requires: gdb python3

%prep
%setup -n pystack

%build
ENVIRON='. %i/etc/profile.d/init.sh' \
PYGDBINIT=$(perl -ne 's/^\s*#.*//; s/[ \t]+$//; s/([\$\`\\])/\\$1/g; /^$/ || print' < .pygdbinit) \
perl -p -i -e 's/\@(ENVIRON|PYGDBINIT)\@/$ENV{$1}/' pystack

(echo '#!/bin/sh'
 echo '. %i/etc/profile.d/init.sh'
 echo 'exec $GDB_ROOT/bin/gdb ${1+"$@"}') > gdb
chmod 755 gdb

%install
mkdir -p %i/bin
cp -p pystack gdb %i/bin

%post
