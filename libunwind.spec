### RPM external libunwind 0.99
Source: http://download.savannah.nongnu.org/releases/libunwind/%n-%realversion.tar.gz
Patch0: libunwind-cleanup
Patch1: libunwind-optimise

%prep
%setup -n %n-%realversion
%patch0 -p0
%patch1 -p0
# Linker visibility attributes don't work with SL4 binutils.
perl -p -i -e 's/__attribute__\s*\(\(visibility\s*\("[a-z]+"\)\)\)//' include/libunwind_i.h

%build
./configure --prefix=%i
make %makeprocesses

%install
make install
