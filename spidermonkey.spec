### RPM external spidermonkey 1.8.5
Source: http://ftp.mozilla.org/pub/mozilla.org/js/js185-1.0.0.tar.gz
Patch: spidermonkey-osx-va-copy
Requires: python

%prep
%setup -n js-%realversion
%patch -p0

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
