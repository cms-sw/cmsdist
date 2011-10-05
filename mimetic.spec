### RPM external mimetic 0.9.6
Source: http://codesink.org/download/%{n}-%{realversion}.tar.gz
Patch0: mimetic-0.9.5-amd64-uint
Patch1: mimetic-0.9.6-uint32_t-gcc44
Patch2: mimetic-0.9.6-fix-gcc47

%prep
%setup -n %n-%{realversion}

%patch0 -p1
case %cmsplatf in
  *_gcc4[0123]*) ;;
  *)
%patch1 -p1
%patch2 -p1
  ;;
esac

%build
./configure --prefix=%i --disable-static
make

%install
make install
