### RPM external mongo 2.0.7

Patch: mongo-osx
Source: http://downloads.mongodb.org/src/mongodb-src-r%{realversion}.tar.gz
Requires: boost scons pcre spidermonkey rotatelogs

Provides: libpcap.so.0.8.3
Provides: libpcap.so.0.8.3()(64bit)

%prep
%setup -n mongodb-src-r%{realversion}
perl -p -i -e 's/-rdynamic//' SConstruct
perl -p -i -e 's/"-mt"/""/' SConstruct
%patch

# scons apparently removes $PATH and $LD_LIBRARY_PATH when invoking
# compiler commands, so force the environment back -- gcc needs it.
# this isn't actually quite enough as scons also forces -L/lib64
# type options straight into command line, with -lstdc++, etc., so
# linking is also likely somewhat broken.
cat > scons-cxx-wrapper << EOFCXX
#!/bin/sh
%if "%{?use_system_gcc:set}" != "set"
. $GCC_ROOT/etc/profile.d/init.sh
%endif

# Boost 1.46.0 has a bug on boost filesystem3, so we set to use filesystem2 instead.
# See http://www.freeorion.org/forum/viewtopic.php?f=24&t=5180
#
# We also get rid of deprecated bits that lead to compile warnings. See
# http://stackoverflow.com/questions/1814548/boostsystem-category-defined-but-not-used
exec c++ -DBOOST_SYSTEM_NO_DEPRECATED -DBOOST_FILESYSTEM_VERSION=2 \${1+"\$@"}
EOFCXX
chmod 755 scons-cxx-wrapper

cat > scons-cc-wrapper << EOFCC
#!/bin/sh
%if "%{?use_system_gcc:set}" != "set"
. $GCC_ROOT/etc/profile.d/init.sh
%endif
exec cc -DBOOST_SYSTEM_NO_DEPRECATED -DBOOST_FILESYSTEM_VERSION=2 \${1+"\$@"}
EOFCC
chmod 755 scons-cc-wrapper

%build
case $(uname) in
  Darwin ) X64= ;;
  *      ) X64=--64 ;;
esac
#scons %makeprocesses $X64 --cxx=$PWD/scons-cxx-wrapper --cc=$PWD/scons-cc-wrapper --extrapathdyn=$PCRE_ROOT,$BOOST_ROOT,$SPIDERMONKEY_ROOT --prefix=%i all
scons %makeprocesses $X64 --cxx=$PWD/scons-cxx-wrapper --cc=$PWD/scons-cc-wrapper --extrapathdyn=$PCRE_ROOT,$BOOST_ROOT,$SPIDERMONKEY_ROOT --prefix=%i install


%install
case $(uname) in
  Darwin ) X64= ;;
  *      ) X64=--64 ;;
esac
#scons %makeprocesses $X64 --cxx=$PWD/scons-sucks-wrapper --cc=$PWD/scons-cc-wrapper --extrapathdyn=$PCRE_ROOT,$BOOST_ROOT,$SPIDERMONKEY_ROOT --prefix=%i install

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
