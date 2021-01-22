### RPM external curl 7.59.0
Source: http://curl.haxx.se/download/%{n}-%{realversion}.tar.gz
Requires: zlib

%prep
%setup -n %{n}-%{realversion}

%build
case %{cmsplatf} in
  osx*) KERBEROS_ROOT=/usr/heimdal ;;
  *) KERBEROS_ROOT=/usr ;;
esac

./configure \
  --prefix=%{i} \
  --disable-silent-rules \
  --disable-static \
  --without-libidn \
  --disable-ldap \
  --with-zlib=${ZLIB_ROOT} \
  --without-nss \
  --without-libssh2 \
  --with-gssapi=${KERBEROS_ROOT}

make %{makeprocesses}

%install
make install
case %{cmsos} in 
  osx*) SONAME=dylib ;;
  *) SONAME=so ;;
esac

# Trick to get our version of curl pick up our version of its associated shared
# library (which is different from the one coming from the system!).
%ifos darwin
install_name_tool -id %{i}/lib/libcurl-cms.dylib -change %{i}/lib/libcurl.4.dylib %{i}/lib/libcurl-cms.dylib  %{i}/lib/libcurl.4.dylib
install_name_tool -change %{i}/lib/libcurl.4.dylib %{i}/lib/libcurl-cms.dylib %{i}/bin/curl
ln -s libcurl.4.dylib %{i}/lib/libcurl-cms.dylib
%endif

# Remove pkg-config to avoid rpm-generated dependency on /usr/bin/pkg-config
# which we neither need nor use at this time.
rm -rf %{i}/lib/pkgconfig

# Strip libraries, we are not going to debug them.
%define strip_files %{i}/lib
# Read documentation online.
%define drop_files %{i}/share

%post
%{relocateConfig}bin/curl-config
