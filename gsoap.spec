### RPM external gsoap 2.7.6e
Source: http://switch.dl.sourceforge.net/sourceforge/gsoap2/%{n}_%{v}.tar.gz
%prep
%setup -n %{n}-%(echo %v | cut -d. -f1,2)
%build
./configure --prefix=%{i}
make 
