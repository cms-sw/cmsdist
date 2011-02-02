### RPM external bz2lib 1.0.5
# Build system patches by Lassi A. Tuura <lat@iki.fi>
Source: http://www.bzip.org/%realversion/bzip2-%realversion.tar.gz
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
# For bzip2 1.0.5, the library appears to retain the name libbz2.so.1.0.4
# rather than libbz2.so.1.0.5 as one would expect, so use this "tmpversion"
# instead of realversion
%define tmpversion 1.0.4
cp libbz2.$so.%tmpversion %i/lib
ln -s libbz2.$so.%tmpversion %i/lib/libbz2.$so
ln -s libbz2.$so.%tmpversion %i/lib/libbz2.$so.`echo %tmpversion | cut -d. -f 1,2`
ln -s libbz2.$so.%tmpversion %i/lib/libbz2.$so.`echo %tmpversion | cut -d. -f 1`

# SCRAM ToolBox toolfile
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/%n
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=%n version=%v>
<info url="http://sources.redhat.com/bzip2/"></info>
<lib name=bz2>
<Client>
 <Environment name=BZ2LIB_BASE default="%i"></Environment>
 <Environment name=LIBDIR default="$BZ2LIB_BASE/lib"></Environment>
 <Environment name=INCLUDE default="$BZ2LIB_BASE/include"></Environment>
</Client>
</Tool>
EOF_TOOLFILE

%post
%{relocateConfig}etc/scram.d/%n
