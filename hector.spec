### RPM external hector 1_3_4

%define mic %(case %cmsplatf in (*_mic_*) echo true;; (*) echo false;; esac)
%if "%mic" == "true"
Requires: icc
%endif
%define rname Hector
%define realversion %(echo %v | cut -d- -f1 )
Requires: root
Source: http://cmsrep.cern.ch/cmssw/cms/SOURCES/slc5_amd64_gcc472/external/hector/1_3_4/Hector_1_3_4.tbz
Patch0: hector-1.3.4-macosx
Patch1: hector-1.3.4-fix-beam-dispersion-macro
Patch2: hector-1.3.4-fix-narrowing-conversion

%if "%{?cms_cxx:set}" != "set"
%define cms_cxx g++
%endif

%if "%{?cms_cxxflags:set}" != "set"
%define cms_cxxflags -std=c++0x
%endif

%prep
%setup -q -n %{rname}_%{realversion}
%patch0 -p2
%patch1 -p1
%patch2 -p1

%build
# On macosx strip -s means something different than on linux.
# We simply ignore the stripping.
perl -p -i -e "s|^.*[@]strip.*\n||" Makefile
# Correct link path for root.
perl -p -i -e "s|^ROOTLIBS.*$|ROOTLIBS=-L$ROOT_ROOT/lib -lCore -lRint -lMatrix -lPhysics -lCint -lMathCore -pthread -lm -ldl -rdynamic|" Makefile
case %cmsplatf in
  *_mic_*)
    perl -p -i -e 's| -lm | -mmic -fPIC |g' Makefile
  ;;
  osx*) perl -p -i -e 's|-rdynamic||g' Makefile ;;
esac

# Add CXX and CXXFLAGS to Makefile and increase output versbose level
sed -ibak "s/@g++/\$(CXX) \$(CXXFLAGS)/g" Makefile

%if "%mic" == "true"
sed -i -e "s/g++/icc /g" Makefile
%define cms_cxx icc
%endif
make %{makeprocesses} CXX="%cms_cxx" CXXFLAGS="%cms_cxxflags"

%install
tar -c . | tar -x -C %i
