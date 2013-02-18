### RPM external libuuid 2.22.2
Source: http://www.kernel.org/pub/linux/utils/util-linux/v2.22/util-linux-%realversion.tar.gz
%define keep_archives true

%prep
%setup -n util-linux-%realversion

%build
./configure $([ $(uname) == Darwin ] && echo --disable-shared) --enable-uuidd --disable-login --disable-su --libdir=%i/lib64 --prefix=%i
make uuidd

%install
# There is no make install action for the libuuid libraries only
mkdir -p %i/lib64
cp -rp %_builddir/util-linux-%realversion/.libs/* %i/lib64/
mkdir -p %i/include
make install-uuidincHEADERS
case %cmsos in
  slc*) ln -sf libuuid.so.1.3.0 %i/lib64/libuuid.so ;;
esac
rm -rf %i/lib64/{pkgconfig,*.la,*.lai}
%define strip_files %i/lib64
%define drop_files %i/man
