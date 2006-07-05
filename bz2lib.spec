### RPM external bz2lib 1.0.2
# Build system patches by Lassi A. Tuura <lat@iki.fi>
Source: ftp://sources.redhat.com/pub/bzip2/v%(echo %v | tr -d .)/bzip2-%v.tar.gz
Provides: libbz2.so.1

%prep
%setup -n bzip2-%v
sed -e 's/ -shared/ -dynamiclib/' \
    -e 's/ -Wl,-soname -Wl,[^ ]*//' \
    -e 's/libbz2\.so/libbz2.dylib/g' \
    < Makefile-libbz2_so > Makefile-libbz2_dylib

%build
case $(uname) in Darwin ) so=dylib ;; * ) so=so ;; esac
make %makeprocesses -f Makefile-libbz2_$so

%install
case $(uname) in Darwin ) so=dylib ;; * ) so=so ;; esac
make install PREFIX=%i
cp libbz2.$so.%v %i/lib
ln -s libbz2.$so.%v %i/lib/libbz2.$so
ln -s libbz2.$so.%v %i/lib/libbz2.$so.`echo %v | cut -d. -f 1,2`
ln -s libbz2.$so.%v %i/lib/libbz2.$so.`echo %v | cut -d. -f 1`
# mimetic.spec
