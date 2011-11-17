### RPM external freetype 2.4.7
Source: http://download.savannah.gnu.org/releases/freetype/freetype-%realversion.tar.bz2
Requires: bz2lib zlib

%prep
%setup -n %n-%realversion

%build
./configure --prefix %{i} --with-bzlib2=$BZ2LIB_ROOT --with-zlib=$ZLIB_ROOT
make %makeprocesses
%install
make install
case %cmsos in
  osx*)
install_name_tool -id %i/lib/libfreetype-cms.dylib -change %i/lib/libfreetype.6.dylib %i/lib/libfreetype-cms.dylib  %i/lib/libfreetype.6.dylib
ln -s libfreetype.6.dylib %i/lib/libfreetype-cms.dylib
perl -p -i -e 's|-lfreetype|-lfreetype-cms|' %i/bin/freetype-config
  ;;
esac

# Strip libraries, we are not going to debug them.
%define strip_files %i/lib
%post
%{relocateConfig}bin/freetype-config
