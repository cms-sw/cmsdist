### RPM external uuid 1.38

# ** Attention **
# This package has been depricated. Use libuuid instead.
# Libuuid is built from the more reliable/update Util-Linux-ng instead of
# e2fsprogs. The package here actually was never properly working, but since
# SL5 boxes came by default with the system libuuid installed, we were fooled.
# On SL6 boxes, however, we don't have the system libuuid installed.
# Therefore we fail to have some symbols not provided by the (old)
# uuid from e2fsprogs.

# Patches by Lassi A. Tuura <lat@iki.fi> (FIXME: contribute to e2fsprogs)
Source: http://switch.dl.sourceforge.net/sourceforge/e2fsprogs/e2fsprogs-%realversion.tar.gz

%define keep_archives true

#Patch0: uuid
#Patch1: uuid-osx

%prep
%setup -n e2fsprogs-%realversion
#%patch0
#%ifos darwin
#%patch1
#endif

%build
./configure $([ $(uname) != Darwin ] && echo --enable-elf-shlibs) --libdir=%i/lib64 --prefix=%i
make lib/ext2fs/ext2_types.h
cd lib/uuid
make

%install
mkdir -p %i/lib64
mkdir -p %i/include
cd lib/uuid
make install
case %cmsos in
  slc*) ln -sf libuuid.so.1.2 %i/lib64/libuuid.so ;;
esac
rm -rf %i/lib64/pkgconfig
%define strip_files %{i}/lib64
%define drop_files %i/man
