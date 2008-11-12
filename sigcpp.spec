### RPM external sigcpp 2.2.3
%define majorv %(echo %realversion | cut -d. -f1,2) 
Source: http://ftp.gnome.org/pub/GNOME/sources/libsigc++/%{majorv}/libsigc++-%{realversion}.tar.gz
#Patch0: sigcpp-2.0.18-gcc42

%prep
%setup -q -n libsigc++-%{realversion}
#case %gccver in
#  4.3.*)
#%patch0 -p2
#  ;;
#esac
./configure --prefix=%{i} 

%build
make %makeprocesses 
%install
make install
cp %i/lib/sigc++-2.0/include/sigc++config.h %i/include/sigc++-2.0/
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
