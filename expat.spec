### RPM external expat 2.4.6
## INITENV +PATH LD_LIBRARY_PATH %{i}/lib64
%define realversion %(echo %v | sed -e 's/\\./_/g')
Source: https://github.com/libexpat/libexpat/releases/download/R_%{realversion}/%{n}-%{v}.tar.gz

Requires: libbsd

%define drop_files %{i}/share

%prep
%setup -n %{n}-%{realversion}

%build
# Update to detect aarch64 and ppc64le
rm -f ./conftools/config.{sub,guess}
%get_config_sub ./conftools/config.sub
%get_config_guess ./conftools/config.guess
chmod +x ./conftools/config.{sub,guess}

./configure --prefix=%{i} --with-libbsd
make %{makeprocesses}

%install
make install
