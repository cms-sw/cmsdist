### RPM external freetype 2.4.7
%define mic %(case %cmsplatf in (*_mic_*) echo true;; (*) echo false;; esac)
%if "%mic" == "true"
Requires: icc
%endif
Source: http://download.savannah.gnu.org/releases/freetype/freetype-%realversion.tar.bz2
Requires: bz2lib zlib

%prep
%setup -n %n-%realversion

%build
case %{cmsplatf} in
   *_mic_* )
     CXX="icpc -fPIC -mmic"  CC="icc -fPIC -mmic" ./configure --prefix %{i} --with-bzlib2=$BZ2LIB_ROOT --with-zlib=$ZLIB_ROOT --host=x86_64-k1om-linux
     ;;
   * )
     ./configure --prefix %{i} --with-bzlib2=$BZ2LIB_ROOT --with-zlib=$ZLIB_ROOT
     ;;
esac
make %makeprocesses
%install
make install
case %cmsos in
  osx*)
install_name_tool -id %i/lib/libfreetype-cms.dylib -change %i/lib/libfreetype.6.dylib %i/lib/libfreetype-cms.dylib  %i/lib/libfreetype.6.dylib
ln -s libfreetype.6.dylib %i/lib/libfreetype-cms.dylib
perl -p -i -e 's|-lfreetype|-lfreetype-cms|' %i/bin/freetype-config
  ;;
  *_mic)
ln -s libfreetype.so %i/lib/libfreetype-cms.so
perl -p -i -e 's|-lfreetype|-lfreetype-cms|' %i/bin/freetype-config
  ;;
esac

# Strip libraries, we are not going to debug them.
%define strip_files %i/lib
%post
%{relocateConfig}bin/freetype-config
