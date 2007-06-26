### RPM external bz2lib 1.0.2-XXXX
# Build system patches by Lassi A. Tuura <lat@iki.fi>
Source: ftp://sources.redhat.com/pub/bzip2/v%(echo %realversion | tr -d .)/bzip2-%realversion.tar.gz
%define cpu %(echo %cmsplatf | cut -f2 -d_)
Provides: libbz2.so.1
%if "%cpu" == "amd64"
Provides: libbz2.so.1()(64bit)
%endif

%prep
%setup -n bzip2-%realversion
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
cp libbz2.$so.%realversion %i/lib
ln -s libbz2.$so.%realversion %i/lib/libbz2.$so
ln -s libbz2.$so.%realversion %i/lib/libbz2.$so.`echo %realversion | cut -d. -f 1,2`
ln -s libbz2.$so.%realversion %i/lib/libbz2.$so.`echo %realversion | cut -d. -f 1`


