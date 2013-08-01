### RPM external mimetic 0.9.6
Source: http://www.codesink.org/download/%{n}-%{realversion}.tar.gz
Patch0: mimetic-0.9.5-amd64-uint
Patch1: mimetic-0.9.6-uint32_t-gcc44
Patch2: mimetic-0.9.6-fix-gcc47-cxx11

%if "%{?cms_cxx:set}" != "set"
%define cms_cxx g++
%endif

%if "%{?cms_cxxflags:set}" != "set"
%define cms_cxxflags -O2 -std=c++0x
%endif

%prep
%setup -n %n-%{realversion}

%patch0 -p1
case %cmsplatf in
  *_gcc4[0123]*) ;;
  *)
%patch1 -p1
  ;;
esac

# Apply C++11 / gcc 4.7.x fixes only if using a 47x architecture.
# See http://gcc.gnu.org/gcc-4.7/porting_to.html
case %cmsplatf in
  *gcc4[789]*)
%patch2 -p1
  ;;
esac

%build
./configure --prefix=%i --disable-static CXX="%cms_cxx" CXXFLAGS="%cms_cxxflags"
make

%install
make install
