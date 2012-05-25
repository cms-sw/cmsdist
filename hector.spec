### RPM external hector 1_3_4

%define rname Hector
%define realversion %(echo %v | cut -d- -f1 )
Requires: root
Source: http://www.fynu.ucl.ac.be/themes/he/ggamma/hector/%{rname}_%{realversion}.tbz
Patch0: hector-1.3.4-macosx

%if "%{?cms_cxx:set}" != "set"
%define cms_cxx g++
%endif

%if "%{?cms_cxxflags:set}" != "set"
%define cms_cxxflags -std=c++0x
%endif

%prep
%setup -q -n %{rname}_%{realversion}
%patch0 -p2

%build
# On macosx strip -s means something different than on linux.
# We simply ignore the stripping.
perl -p -i -e "s|^.*[@]strip.*\n||" Makefile
# Correct link path for root.
perl -p -i -e "s|^ROOTLIBS.*$|ROOTLIBS=-L$ROOT_ROOT/lib -lCore -lRint -lMatrix -lPhysics -lCint -lMathCore -pthread -lm -ldl -rdynamic|" Makefile
case %cmsplatf in
  osx*) perl -p -i -e 's|-rdynamic||g' Makefile ;;
esac

# Add CXX and CXXFLAGS to Makefile and increase output versbose level
sed -ibak "s/@g++/\$(CXX) \$(CXXFLAGS)/g" Makefile

make CXX="%cms_cxx" CXXFLAGS="%cms_cxxflags"

%install
tar -c . | tar -x -C %i
