### RPM external mcdb 1.0.2
Source: http://mcdb.cern.ch/distribution/api/%{n}-api-%{realversion}.tar.gz
Requires: xerces-c
Patch0: mcdb-1.0.2-gcc45

%if "%{?cms_cxx:set}" != "set"
%define cms_cxx g++
%endif

%if "%{?cms_cxxflags:set}" != "set"
%define cms_cxxflags -O2 -std=c++0x
%endif

%prep
%setup -q -n %{n}-api-%{realversion}

case %gccver in
  4.5.* | 4.6.* | 4.7.*)
%patch0 -p1
  ;;
esac

rm config.mk
touch config.mk
case %cmsplatf in
  osx*) 
echo "PLATFORM = %cmsplatf" >> config.mk
echo "CC       = gcc" >> config.mk
echo "CXX      = %cms_cxx" >> config.mk
echo "CFLAGS   = -O2 -pipe -Wall -W -fPIC" >> config.mk
echo "CXXFLAGS = %cms_cxxflags -pipe -Wall -W -fPIC" >> config.mk
echo "LINK     = %cms_cxx" >> config.mk
echo "LFLAGS   = -dynamiclib " >> config.mk
echo "XERCESC  = $XERCES_C_ROOT" >> config.mk
;;
  *ia32*  ) 
echo "PLATFORM = %cmsplatf" >> config.mk
echo "CC       = gcc" >> config.mk
echo "CXX      = %cms_cxx" >> config.mk
echo "CFLAGS   = -O2 -pipe -Wall -W -march=i386 -mtune=i686 -fPIC" >> config.mk
echo "CXXFLAGS = %cms_cxxflags -pipe -Wall -W -march=i386 -mtune=i686 -fPIC" >> config.mk
echo "LINK     = %cms_cxx" >> config.mk
echo "LFLAGS   = -shared -Wl,-soname,libmcdb.so" >> config.mk
echo "XERCESC  = $XERCES_C_ROOT" >> config.mk
;;
  *amd64* ) 
echo "PLATFORM = %cmsplatf" >> config.mk
echo "CC       = gcc" >> config.mk
echo "CXX      = %cms_cxx" >> config.mk
echo "CFLAGS   = -O2 -pipe -Wall -W -fPIC" >> config.mk
echo "CXXFLAGS = %cms_cxxflags -pipe -Wall -W -fPIC" >> config.mk
echo "LINK     = %cms_cxx" >> config.mk
echo "LFLAGS   = -shared -Wl,-soname,libmcdb.so" >> config.mk
echo "XERCESC  = $XERCES_C_ROOT" >> config.mk
;;
  *       )    # This default is bogus, needs specification for each non-linux
echo "PLATFORM = %cmsplatf" >> config.mk
echo "CC       = gcc" >> config.mk
echo "CXX      = %cms_cxx" >> config.mk
echo "CFLAGS   = -O2 -pipe -Wall -W -march=i386 -mtune=i686 -fPIC" >> config.mk
echo "CXXFLAGS = %cms_cxxflags -pipe -Wall -W -march=i386 -mtune=i686 -fPIC" >> config.mk
echo "LINK     = %cms_cxx" >> config.mk
echo "LFLAGS   = -shared -Wl,-soname,libmcdb.so" >> config.mk
echo "XERCESC  = $XERCES_C_ROOT" >> config.mk
;;
esac




%build
make

%install
tar -c lib interface | tar -x -C %i
