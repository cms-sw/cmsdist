### RPM external zlib 1.2.8
%define mic %(case %cmsplatf in (*_mic_*) echo true;; (*) echo false;; esac)
%if "%mic" == "true"
Requires: icc
%endif
Source: http://zlib.net/%{n}-%{realversion}.tar.gz

%prep
%setup -n %{n}-%{realversion}

%build

case %{cmsplatf} in
   *_mic_* )
     CHOST=x86_64-k1om-linux  CC="icc -fPIC -mmic" ./configure --prefix=%{i}
     ;;
   *_amd64_gcc4[56789]* )
     CFLAGS="-fPIC -O3 -DUSE_MMAP -DUNALIGNED_OK -D_LARGEFILE64_SOURCE=1 -msse3" \
     ./configure --prefix=%{i}
     ;;
   *_armv7hl_gcc4[56789]* )
     CFLAGS="-fPIC -O3 -DUSE_MMAP -DUNALIGNED_OK -D_LARGEFILE64_SOURCE=1" \
     ./configure --prefix=%{i}
     ;;
   * )
     %{cfgopts} ./configure --prefix=%{i}
     ;;
esac

make %{makeprocesses}

# Strip libraries, we are not going to debug them.
%define strip_files %{i}/lib
# Look up documentation online.
%define drop_files %{i}/share
