### RPM external freetype 2.5.3
Source: http://download.savannah.gnu.org/releases/freetype/freetype-%{realversion}.tar.bz2
Requires: bz2lib zlib libpng

%prep
%setup -n %{n}-%{realversion}

%build
./configure \
  --prefix %{i} \
  --with-bzip2==${BZ2LIB_ROOT} \
  --with-zlib=${ZLIB_ROOT} \
  --with-png=${LIBPNG_ROOT} \
  --with-harfbuzz=no

make %{makeprocesses}

%install
make install
%ifos darwin
install_name_tool -id %{i}/lib/libfreetype-cms.dylib -change %{i}/lib/libfreetype.6.dylib %{i}/lib/libfreetype-cms.dylib %{i}/lib/libfreetype.6.dylib
ln -s libfreetype.6.dylib %{i}/lib/libfreetype-cms.dylib
perl -p -i -e 's|-lfreetype|-lfreetype-cms|' %{i}/bin/freetype-config
%endif

# Strip libraries, we are not going to debug them.
%define strip_files %{i}/lib
%post
%{relocateConfig}bin/freetype-config
# bla bla
