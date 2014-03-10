### RPM external blackhat 0.9.9
Source: http://www.hepforge.org/archive/blackhat/blackhat-%{realversion}.tar.gz

Patch0: blackhat-gcc48

Requires: qd python
%prep
%setup -n blackhat-%{realversion}

%patch0 -p1

./configure --prefix=%i --with-QDpath=$QD_ROOT CXXFLAGS="-Wno-deprecated"
# The following hack insures that the bins with the library linked explicitly
# rather than indirectly, as required by the gold linker
%build
make %{makeprocesses}
%install
make install
