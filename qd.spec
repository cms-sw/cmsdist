### RPM external qd 2.3.13
Source: http://crd.lbl.gov/~dhbailey/mpdist/qd-%{realversion}.tar.gz

%prep
%setup -n qd-%{realversion}

# Update to detect aarch64 and ppc64le
rm -f ./config/config.{sub,guess}
%get_config_sub ./config/config.sub
%get_config_guess ./config/config.guess
chmod +x ./config/config.{sub,guess}

./configure --prefix=%{i} --enable-shared

%build
make %{makeprocesses}

%install
make install
