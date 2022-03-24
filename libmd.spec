### RPM external libmd 1.0.3
Source: https://archive.hadrons.org/software/libmd/%{n}-%{v}.tar.xz

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