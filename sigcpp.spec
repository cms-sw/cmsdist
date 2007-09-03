### RPM external sigcpp 2.0.17-CMS8
%define majorv %(echo %realversion | cut -d. -f1,2) 
Source: http://ftp.gnome.org/pub/GNOME/sources/libsigc++/%{majorv}/libsigc++-%{realversion}.tar.gz

%prep
%setup -q -n libsigc++-%{realversion}
./configure --prefix=%{i} 

%build
make %makeprocesses 
%install
make install
cp %i/lib/sigc++-%{majorv}/include/sigc++config.h %i/include/sigc++-%{majorv}/
# SCRAM ToolBox toolfile
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/%n
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=sigcpp version=%v>
<lib name=sigc-2.0>
<Client>
 <Environment name=SIGCPP_BASE default="%i"></Environment>
 <Environment name=LIBDIR default="$SIGCPP_BASE/lib"></Environment>
 <Environment name=INCLUDE default="$SIGCPP_BASE/include/sigc++-2.0"></Environment>
</Client>
</Tool>
EOF_TOOLFILE

%post
%{relocateConfig}etc/scram.d/%n
