### RPM cms pystack 1.0
Source: svn://svn.cern.ch/reps/CMSDMWM/HTTPGroup/tags/3.2?scheme=svn+ssh&strategy=export&module=HTTPGroup&output=/src.tar.gz
Requires: gdb python

%prep
%setup -n HTTPGroup/Tools

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

# Generate dependencies-setup.{sh,csh} so init.{sh,csh} picks full environment.
rm -fr %i/etc/profile.d
mkdir -p %i/etc/profile.d
for tool in $(echo %{requiredtools} | sed -e's|\s+| |;s|^\s+||'); do
  root=$(echo $tool | tr a-z- A-Z_)_ROOT; eval r=\$$root
  if [ X"$r" != X ] && [ -r "$r/etc/profile.d/init.sh" ]; then
    echo "test X\$$root != X || . $r/etc/profile.d/init.sh" >> %i/etc/profile.d/dependencies-setup.sh
    echo "test X\$$root != X || source $r/etc/profile.d/init.csh" >> %i/etc/profile.d/dependencies-setup.csh
  fi
done

%post
%{relocateConfig}etc/profile.d/dependencies-setup.*sh
%{relocateConfig}bin/{pystack,gdb}
