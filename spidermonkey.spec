### RPM external spidermonkey 1.8.0_rc1
Source: http://ftp.mozilla.org/pub/mozilla.org/js/js-1.8.0-rc1.tar.gz
Patch: spidermonkey-osx-va-copy

%prep
%setup -n js
%patch -p1

%build
cd src
if [ `uname -m` != 'x86_64' ]; then
    LDEMULATION=elf_i386 make -f Makefile.ref
else
    make LD='$(CC)' -f Makefile.ref
fi

%install
cd src
mkdir -p %i/bin
cp *_DBG.OBJ/{js,jscpucfg,jskwgen} %i/bin
mkdir -p %i/lib
cp *_DBG.OBJ/libjs* %i/lib
mkdir -p %i/include/{editline,fdlibm,liveconnect}
cp jsproto.tbl %i/include
cp *.h %i/include
cp *_DBG.OBJ/*.h %i/include
cp editline/*.h %i/include/editline
cp fdlibm/*.h %i/include/fdlibm
cp liveconnect/*.h %i/include/liveconnect
cd %i/lib
ln -s libjs.a libjs_static.a

%define strip_files %i/lib

%post
%{relocateConfig}/bin/js
%{relocateConfig}/bin/jscpucfg
%{relocateConfig}/bin/jskwgen

