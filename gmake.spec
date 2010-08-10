### RPM external gmake 3.81
# We will call it "gmake", but gnu calls it "make"
Source: ftp://ftp.gnu.org/gnu/make/make-%realversion.tar.gz
Patch0: gmake-3.81-expand

%prep
%setup -n make-%{realversion}
%patch0 -p1

%build
./configure --prefix=%i

make %makeprocesses

%install
make install
# Put in the symlink
cd %{i}/bin
ln -sf make gmake

# SCRAM ToolBox toolfile
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/%n.xml
  <tool name="%n" version="%v">
    <client>
      <environment name="MAKE_BASE" default="%i"/>
    </client>
    <runtime name="PATH" value="$MAKE_BASE/bin" type="path"/>
  </tool>
EOF_TOOLFILE

%post
%{relocateConfig}etc/scram.d/%n.xml

