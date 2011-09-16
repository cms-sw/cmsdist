### RPM external uuid 1.38
# Patches by Lassi A. Tuura <lat@iki.fi> (FIXME: contribute to e2fsprogs)
Source: http://switch.dl.sourceforge.net/sourceforge/e2fsprogs/e2fsprogs-%realversion.tar.gz

#Patch0: uuid
#Patch1: uuid-osx

%prep
%setup -n e2fsprogs-%realversion
#%patch0
#%ifos darwin
#%patch1
#endif

%build
./configure $([ $(uname) != Darwin ] && echo --enable-elf-shlibs) --prefix=%i
make lib/ext2fs/ext2_types.h
cd lib/uuid
make

%install
mkdir -p %i/lib
mkdir -p %i/include
cd lib/uuid
make install
ln -sf libuuid.so.1.2 %i/lib/libuuid.so
# Remove pkg-config to avoid rpm-generated dependency on /usr/bin/pkg-config
# which we neither need nor use at this time.
rm -rf %i/lib/pkgconfig

# Strip libraries, we are not going to debug them.
find %i/lib -type f -perm -a+x -exec strip {} \;

# Don't need archive libraries.
rm -f %i/lib/*.{l,}a

# Look up documentation online.
rm -rf %i/man
