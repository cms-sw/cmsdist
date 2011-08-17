### RPM external mimetic 0.9.6
Source: http://codesink.org/download/%{n}-%{realversion}.tar.gz
Patch0: mimetic-0.9.5-amd64-uint
Patch1: mimetic-0.9.6-uint32_t-gcc44

%prep
%setup -n %n-%{realversion}

case %cmsplatf in
*gcc4* | osx*)
%patch0 -p1
esac

case %gccver in
  4.4.* | 4.5.* | 4.6.*)
%patch1 -p1
  ;;
esac

%build
./configure --prefix=%i --disable-static
make

%install
make install
