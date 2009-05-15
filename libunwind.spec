### RPM external libunwind 0.99
Source: http://download.savannah.nongnu.org/releases/libunwind/%n-%realversion.tar.gz

%prep
%setup -n %n-%realversion
# Linker visibility attributes don't work with SL4 binutils.
perl -p -i -e 's/__attribute__\s*\(\(visibility\s*\("[a-z]+"\)\)\)//' include/libunwind_i.h

%build
./configure --prefix=%i
make %makeprocesses

%install
make install
mkdir -p %i/etc/scram.d
sed 's/^  //' > %i/etc/scram.d/%n << \EOF
  <doc type=BuildSystem::ToolDoc version=1.0>
  <Tool name="%n" version="%v">
    <info url="http://www.nongnu.org/libunwind/"></info>
    <lib name=unwind>
    <Client>
      <Environment name=UNWIND_BASE default="%i"></Environment>
      <Environment name=LIBDIR default="$UNWIND_BASE/lib"></Environment>
      <Environment name=INCLUDE default="$UNWIND_BASE/include"></Environment>
    </Client>
  </Tool>
EOF

%post
%{relocateConfig}etc/scram.d/%n
