### RPM external mongo 1.4.0
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

## IMPORT common-install

%post
## IMPORT common-post

