### RPM external hector 1.3.4
%define tag 365361cb7771593c2ff0ad91aa842858d44ded6d
%define branch cms/v%{realversion}
%define github_user cms-externals
Source: git+https://github.com/%github_user/%{n}.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz
Requires: root

%if "%{?cms_cxx:set}" != "set"
%define cms_cxx g++
%endif

%if "%{?cms_cxxflags:set}" != "set"
%define cms_cxxflags -std=c++11
%endif

%prep
%setup -q -n %{n}-%{realversion}
mkdir -p obj lib

%build
# On macosx strip -s means something different than on linux.
# We simply ignore the stripping.
perl -p -i -e "s|^.*[@]strip.*\n||" Makefile
# Correct link path for root.
#perl -p -i -e "s|^ROOTLIBS.*$|ROOTLIBS=-L$ROOT_ROOT/lib -lCore -lRint -lMatrix -lPhysics -lCling -lMathCore -pthread -lm -ldl -rdynamic|" Makefile
case %cmsplatf in
  osx*) perl -p -i -e 's|-rdynamic||g' Makefile ;;
esac

# Add CXX and CXXFLAGS to Makefile and increase output versbose level
sed -ibak "s/@g++/\$(CXX) \$(CXXFLAGS)/g" Makefile

make CXX="%cms_cxx" CXXFLAGS="%cms_cxxflags"

%install
tar -c . | tar -x -C %i
