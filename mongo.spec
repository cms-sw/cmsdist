### RPM external mongo 1.4.1
## INITENV +PATH PYTHONPATH %i/lib/python`echo $PYTHON_VERSION | cut -d. -f 1,2`/site-packages 

Provides: libpcap.so.0.8.3
# 64-bit versions
Provides: libpcap.so.0.8.3()(64bit)
Source: http://downloads.mongodb.org/src/mongodb-src-r%{realversion}.tar.gz
Requires: boost scons pcre spidermonkey

%prep
%setup -n mongodb-src-r%{realversion}

%build
export CXX=$GCC_ROOT/bin/g++
#scons --64 --cxx=$CXX --extrapath=$PCRE_ROOT,$BOOST_ROOT,$SPIDERMONKEY_ROOT all
scons --64 --cxx=$CXX --extrapathdyn=$PCRE_ROOT,$BOOST_ROOT,$SPIDERMONKEY_ROOT all

%install
export CXX=$GCC_ROOT/bin/g++
#scons --64 --cxx=$CXX --extrapath=$PCRE_ROOT,$BOOST_ROOT,$SPIDERMONKEY_ROOT --prefix=%i install
scons --64 --cxx=$CXX --extrapathdyn=$PCRE_ROOT,$BOOST_ROOT,$SPIDERMONKEY_ROOT --prefix=%i install

# setup dependencies environment
rm -rf %i/etc/profile.d
mkdir -p %i/etc/profile.d
for x in %pkgreqs; do
  case $x in /* ) continue ;; esac
  p=%{instroot}/%{cmsplatf}/$(echo $x | sed 's/\([^+]*\)+\(.*\)+\([A-Z0-9].*\)/\1 \2 \3/' | tr ' ' '/')
  echo ". $p/etc/profile.d/init.sh" >> %i/etc/profile.d/dependencies-setup.sh
  echo "source $p/etc/profile.d/init.csh" >> %i/etc/profile.d/dependencies-setup.csh
done

%post
# The relocation is also needed because of dependencies
%{relocateConfig}etc/profile.d/dependencies-setup.sh
%{relocateConfig}etc/profile.d/dependencies-setup.csh

. $RPM_INSTALL_PREFIX/%{pkgrel}/etc/profile.d/init.sh
mkdir -p $MONGO_ROOT/db
