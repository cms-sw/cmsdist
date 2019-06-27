### RPM external mcdb 1.0.3
Source: http://mcdb.cern.ch/distribution/api/%{n}-api-%{realversion}.tar.gz
Requires: xerces-c

%prep
%setup -q -n %{n}-api-%{realversion}

rm config.mk
touch config.mk
case %{cmsplatf} in
  osx*) 
    echo "PLATFORM = %cmsplatf" >> config.mk
    echo "CC       = gcc" >> config.mk
    echo "CXX      = g++" >> config.mk
    echo "CFLAGS   = -O2 -pipe -Wall -W -fPIC" >> config.mk
    echo "CXXFLAGS = -O2 -pipe -Wall -W -fPIC" >> config.mk
    echo "LINK     = g++" >> config.mk
    echo "LFLAGS   = -dynamiclib " >> config.mk
    echo "XERCESC  = $XERCES_C_ROOT" >> config.mk
    ;;
  *amd64* ) 
    echo "PLATFORM = %cmsplatf" >> config.mk
    echo "CC       = gcc" >> config.mk
    echo "CXX      = g++" >> config.mk
    echo "CFLAGS   = -O2 -pipe -Wall -W -fPIC" >> config.mk
    echo "CXXFLAGS = -O2 -pipe -Wall -W -fPIC" >> config.mk
    echo "LINK     = g++" >> config.mk
    echo "LFLAGS   = -shared -Wl,-soname,libmcdb.so" >> config.mk
    echo "XERCESC  = $XERCES_C_ROOT" >> config.mk
    ;;
  *aarch64* )
    echo "PLATFORM = %cmsplatf" >> config.mk
    echo "CC       = gcc" >> config.mk
    echo "CXX      = g++" >> config.mk
    echo "CFLAGS   = -O2 -pipe -Wall -W -fPIC" >> config.mk
    echo "CXXFLAGS = -O2 -pipe -Wall -W -fPIC" >> config.mk
    echo "LINK     = g++" >> config.mk
    echo "LFLAGS   = -shared -Wl,-soname,libmcdb.so" >> config.mk
    echo "XERCESC  = $XERCES_C_ROOT" >> config.mk
    ;;
  *ppc64le* )
    echo "PLATFORM = %cmsplatf" >> config.mk
    echo "CC       = gcc" >> config.mk
    echo "CXX      = g++" >> config.mk
    echo "CFLAGS   = -O2 -pipe -Wall -W -fPIC" >> config.mk
    echo "CXXFLAGS = -O2 -pipe -Wall -W -fPIC" >> config.mk
    echo "LINK     = g++" >> config.mk
    echo "LFLAGS   = -shared -Wl,-soname,libmcdb.so" >> config.mk
    echo "XERCESC  = $XERCES_C_ROOT" >> config.mk
    ;;
  *ppc64* )
    echo "PLATFORM = %cmsplatf" >> config.mk
    echo "CC       = gcc" >> config.mk
    echo "CXX      = %cms_cxx" >> config.mk
    echo "CFLAGS   = -O2 -pipe -Wall -W -fPIC" >> config.mk
    echo "CXXFLAGS = %cms_cxxflags -pipe -Wall -W -fPIC" >> config.mk
    echo "LINK     = %cms_cxx" >> config.mk
    echo "LFLAGS   = -shared -Wl,-soname,libmcdb.so" >> config.mk
    echo "XERCESC  = " >> config.mk
    ;;
  *armv7hl* )
    echo "PLATFORM = %{cmsplatf}" >> config.mk
    echo "CC       = gcc" >> config.mk
    echo "CXX      = g++" >> config.mk
    echo "CFLAGS   = -O2 -pipe -Wall -W -march=armv7-a -mtune=generic-armv7-a -fPIC" >> config.mk
    echo "CXXFLAGS = -O2 -pipe -Wall -W -march=armv7-a -mtune=generic-armv7-a -fPIC" >> config.mk
    echo "LINK     = g++" >> config.mk
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
# bla bla
