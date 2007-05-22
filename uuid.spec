### RPM external uuid 1.38-XXXX
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
%post
ln -sf $RPM_INSTALL_PREFIX/%cmsplatf/external/%n/%v/lib/libuuid.so.1.2 $RPM_INSTALL_PREFIX/%cmsplatf/external/%n/%v/lib/libuuid.so
