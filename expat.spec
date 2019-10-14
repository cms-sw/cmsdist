### RPM external expat 2.1.0
## INITENV +PATH LD_LIBRARY_PATH %{i}/lib64
Source: http://downloads.sourceforge.net/project/%{n}/%{n}/%{realversion}/%{n}-%{realversion}.tar.gz

%define drop_files %{i}/share

%prep
%setup -n %{n}-%{realversion}

%build
# Update to detect aarch64 and ppc64le
rm -f ./conftools/config.{sub,guess}
%get_config_sub ./conftools/config.sub
%get_config_guess ./conftools/config.guess
chmod +x ./conftools/config.{sub,guess}

./configure --prefix=%{i} 
make %{makeprocesses}

%install
make install
