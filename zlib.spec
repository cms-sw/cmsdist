### RPM external zlib 1.2.3-CMS18
Source: http://www.gzip.org/%n/%n-%realversion.tar.bz2
Patch: zlib-1.2.3-shared-for-32-bit-on-x86_64

%prep
%setup -n %n-%realversion
# Apply this patch to force shared libraries to be created. The problem
# only appears when building 32-bit on 64-bit machines (./configure gets
# confused by the 'skipping /usr/lib64' message), but applying it on all
# linux builds should not hurt since they all should build shared libraries.
%ifos linux
%patch -p1
%endif

%build
case $(uname) in
  Darwin )
    LDSHARED="gcc -dynamiclib" ./configure --shared --prefix=%i
    make LIBS='libz.dylib.$(VER)' SHAREDLIB=libz.dylib # FIXME: libz.$(VER).dylib
    ;;

  * )
    ./configure --shared --prefix=%i
    make %makeprocesses
    ;;
esac

%install
case $(uname) in
  Darwin ) make install LIBS='libz.dylib.$(VER)' SHAREDLIB=libz.dylib ;;
  * ) make install ;;
esac
#
# SCRAM ToolBox toolfile
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/%n
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=%n version=%v>
<lib name=z>
<client>
 <Environment name=ZLIB_BASE default="%i"></Environment>
 <Environment name=INCLUDE default="$ZLIB_BASE/include"></Environment>
 <Environment name=LIBDIR  default="$ZLIB_BASE/lib"></Environment>
</client>
</Tool>
EOF_TOOLFILE

%post
%{relocateConfig}etc/scram.d/%n
