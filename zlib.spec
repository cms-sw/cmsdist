### RPM external zlib 1.2.3
Source: http://www.gzip.org/%n/%n-%realversion.tar.bz2

%prep
%setup -n %n-%realversion

%build
%if "%cmscompiler" == "icc"
%define cfgopts CC="icc -fPIC"
%else
%define cfgopts %nil
%endif

case %cmsplatf in
   *_gcc4[56789]* )
     CFLAGS="-fPIC -O3 -DUSE_MMAP -DUNALIGNED_OK -D_LARGEFILE64_SOURCE=1 -msse3" \
     ./configure --shared --prefix=%i
     ;;

   * )
     %cfgopts ./configure --shared --prefix=%i
     ;;
esac

make %makeprocesses

%install
make install

# Strip libraries, we are not going to debug them.
find %i/lib -type f -perm -a+x -exec strip {} \;

# Look up documentation online.
rm -rf %i/share
