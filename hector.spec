### RPM external hector 1.3.4_patch1
%define tag 7498d56fe88d7c26f7c871c55bb9f5d2f0255004
%define branch cms/v%{realversion}
%define github_user cms-externals
Source: git+https://github.com/%github_user/%{n}.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz

Requires: root

%prep
%setup -q -n %{n}-%{realversion}
mkdir -p obj lib

%build
# Correct link path for root.
#perl -p -i -e "s|^ROOTLIBS.*$|ROOTLIBS=-L$ROOT_ROOT/lib -lCore -lRint -lMatrix -lPhysics -lCling -lMathCore -pthread -lm -ldl -rdynamic|" Makefile
case %cmsplatf in
  osx*) perl -p -i -e 's|-rdynamic||g' Makefile ;;
esac

# Add CXX and CXXFLAGS to Makefile and increase output versbose level
sed -ibak "s/@g++/\$(CXX) \$(CXXFLAGS)/g" Makefile

make

%install
tar -c . | tar -x -C %i
# bla bla
