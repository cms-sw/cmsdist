### RPM external spidermonkey 1.8.5
Source: http://ftp.mozilla.org/pub/mozilla.org/js/js185-1.0.0.tar.gz
Patch0: spidermonkey-osx-va-copy
Patch1: spidermonkey-js-1.8.5-c++11
# Alan on 19/05/2021: python seems not to be required in this spec.
# Besides, it breaks our Python3 stack
# Requires: python

%prep
%setup -n js-%realversion
%patch0 -p0
%patch1 -p1

%build
cd js/src
./configure --prefix=%i
make %makeprocesses

%install
cd js/src
make install
ln -sf libmozjs185.so.1.0.0 %i/lib/libmozjs185.so
ln -sf libmozjs185.so.1.0.0 %i/lib/libmozjs185.so.1.0
ln -sf libmozjs185.so.1.0.0 %i/lib/libmozjs185-1.0.so

# Strip libraries, we are not going to debug them.
%define strip_files %i/lib

%post
%{relocateConfig}bin/js-config
