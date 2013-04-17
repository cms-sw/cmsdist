### RPM external urlfetch 1.2
%define svnserver svn://svn.cern.ch/reps/CMSDMWM
%define pkg urlfetch
#Source0: https://github.com/vkuznet/urlfetch/archive/master.tar.gz
Source0: git://github.com/vkuznet/urlfetch?obj=master/%realversion&export=%pkg&output=/%pkg.tar.gz
Requires: erlang rebar rotatelogs

# RPM macros documentation
# http://www.rpm.org/max-rpm/s1-rpm-inside-macros.html
%prep
%setup -c
%setup -T -D -a 0

%build
cd urlfetch
export PATH=$PATH:$REBAR_ROOT/ebin:$ERLANG_ROOT/bin
make

%install
cd urlfetch
cp -r ebin deps src include priv rebar.config start.sh %i

# Generate dependencies-setup.{sh,csh} so init.{sh,csh} picks full environment.
mkdir -p %i/etc/profile.d
: > %i/etc/profile.d/dependencies-setup.sh
: > %i/etc/profile.d/dependencies-setup.csh
for tool in $(echo %{requiredtools} | sed -e's|\s+| |;s|^\s+||'); do
  root=$(echo $tool | tr a-z- A-Z_)_ROOT; eval r=\$$root
  if [ X"$r" != X ] && [ -r "$r/etc/profile.d/init.sh" ]; then
    echo "test X\$$root != X || . $r/etc/profile.d/init.sh" >> %i/etc/profile.d/dependencies-setup.sh
    echo "test X\$$root != X || source $r/etc/profile.d/init.csh" >> %i/etc/profile.d/dependencies-setup.csh
  fi
done

%post
%{relocateConfig}etc/profile.d/dependencies-setup.*sh
