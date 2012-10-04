### RPM cms vdt v0.2.0

Source: svn://svnweb.cern.ch/guest/%{n}/tags/%{realversion}?scheme=http&strategy=export&module=%{n}&output=/%{n}-%{realversion}.tar.gz

BuildRequires: cmake

%if "%{?cms_cxx:set}" != "set"
%define cms_cxx g++
%endif

%define keep_archives true

%prep
%setup -q -n %{n}

%build
cmake . \
  -DCMAKE_CXX_COMPILER="%cms_cxx"

make %makeprocesses VERBOSE=1

%install
# Copy VDT static library to final location
mkdir -p %{i}/lib
cp ./lib/libvdt.a %{i}/lib

# Copy VDT headers to the final location
rsync -av --exclude '*.cmake' ./include %{i}
