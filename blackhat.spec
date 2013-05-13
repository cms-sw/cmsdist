### RPM external blackhat 0.9.9
Source: http://www.hepforge.org/archive/blackhat/blackhat-%{realversion}.tar.gz

Requires: qd python
%prep
%setup -n blackhat-%{realversion}
./configure --prefix=%i --with-QDpath=$QD_ROOT CXXFLAGS="-Wno-deprecated"
# The following hack insures that the bins with the library linked explicitly
# rather than indirectly, as required by the gold linker
%build
make %{makeprocesses}
%install
make install
rm -f %{i}/lib/blackhat/*.la

%post
%{relocateRpmPkg}bin/blackhat-config
%{relocateRpmPkg}bin/dataInstall
