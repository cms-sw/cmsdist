### RPM external mcdb 1.0.3
Source: http://mcdb.cern.ch/distribution/api/%{n}-api-%{realversion}.tar.gz
Requires: xerces-c
#Patch0: mcdb-1.0.2-gcc45

%if "%{?cms_cxx:set}" != "set"
%define cms_cxx g++
%endif

%if "%{?cms_cxxflags:set}" != "set"
%define cms_cxxflags -O2 -std=c++0x
%endif

%prep
%setup -q -n %{n}-api-%{realversion}
#%patch0 -p1

rm config.mk
touch config.mk
case %{cmsplatf} in
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
  *armv7hl* )
    echo "PLATFORM = %{cmsplatf}" >> config.mk
    echo "CC       = gcc" >> config.mk
    echo "CXX      = %{cms_cxx}" >> config.mk
    echo "CFLAGS   = -O2 -pipe -Wall -W -march=armv7-a -mtune=generic-armv7-a -fPIC" >> config.mk
    echo "CXXFLAGS = %{cms_cxxflags} -pipe -Wall -W -march=armv7-a -mtune=generic-armv7-a -fPIC" >> config.mk
    echo "LINK     = %{cms_cxx}" >> config.mk
    echo "LFLAGS   = -shared -Wl,-soname,libmcdb.so" >> config.mk
    echo "XERCESC  = ${XERCES_C_ROOT}" >> config.mk
    ;;
  *)
    echo "Unsupported build configuration. Review SPEC file."
    exit 1
  ;;
esac

%build
make

%install
tar -c lib interface | tar -x -C %i
