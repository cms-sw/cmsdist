### RPM external spidermonkey 1.8.0_rc1
Source: http://ftp.mozilla.org/pub/mozilla.org/js/js-1.8.0-rc1.tar.gz

%prep
%setup -n js

%build
cd src
if [ `uname -m` != 'x86_64' ]; then
    LDEMULATION=elf_i386 make -f Makefile.ref
else
    make -f Makefile.ref
fi

%install
cd src
mkdir -p %i/bin
cp Linux_All_DBG.OBJ/{js,jscpucfg,jskwgen} %i/bin
mkdir -p %i/lib
cp Linux_All_DBG.OBJ/libjs* %i/lib
mkdir -p %i/include/{editline,fdlibm,liveconnect}
cp jsproto.tbl %i/include
cp *.h %i/include
cp Linux_All_DBG.OBJ/*.h %i/include
cp editline/*.h %i/include/editline
cp fdlibm/*.h %i/include/fdlibm
cp liveconnect/*.h %i/include/liveconnect
cd %i/lib
ln -s libjs.a libjs_static.a

%post
%{relocateConfig}/bin/js
%{relocateConfig}/bin/jscpucfg
%{relocateConfig}/bin/jskwgen

