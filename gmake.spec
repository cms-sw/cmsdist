### RPM external gmake 3.81-CMS19
# We will call it "gmake", but gnu calls it "make"
Source: ftp://ftp.gnu.org/gnu/make/make-%realversion.tar.gz
Patch1: gmake-3.81-expand

%prep
%setup -n make-%{realversion}
%patch1 -p0

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
cat << \EOF_TOOLFILE >%i/etc/scram.d/%n
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=%n version=%v>
<Client>
 <Environment name=MAKE_BASE default="%i"></Environment>
</Client>
<Runtime name=PATH value="$MAKE_BASE/bin" type=path>
</Tool>
EOF_TOOLFILE

%post
cd $RPM_INSTALL_PREFIX/%cmsplatf/external/%n/%v/bin
%{relocateConfig}etc/scram.d/%n

