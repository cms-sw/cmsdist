### RPM external libhepml 0.2.1
Source: http://mcdb.cern.ch/distribution/api/%{n}-%{realversion}.tar.gz
Patch0: libhepml-0.2.1-gcc43
Patch1: libhepml-0.2.1-leopard

%prep
%setup -q -n %{n}-%{realversion}
%patch0 -p2
case %cmsplatf in
  osx*)
%patch1 -p1
  ;;
esac

%build
cd src

make
mv *.so ../lib/.

%install
tar -c lib interface | tar -x -C %i
# bla bla
