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
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/%n.xml
  <tool name="%n" version="%v">
    <info url="http://www.nongnu.org/libunwind/"/>
    <lib name="unwind"/>
    <client>
      <environment name="LIBUNWIND_BASE" default="%i"/>
      <environment name="LIBDIR" default="$LIBUNWIND_BASE/lib"/>
      <environment name="INCLUDE" default="$LIBUNWIND_BASE/include"/>
    </client>
  </tool>
EOF

%post
%{relocateConfig}etc/scram.d/%n.xml
