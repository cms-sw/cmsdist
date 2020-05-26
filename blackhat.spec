### RPM external blackhat 0.9.9
%define tag 3e8ac1f06ef3612088505de448c8e127157076a7
%define branch cms/v%{realversion}
%define github_user cms-externals
Source: git+https://github.com/%{github_user}/%{n}.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}-%{tag}.tgz
Requires: qd python openssl

%prep
%setup -n %{n}-%{realversion}

sed -i -e 's|else return Cached_OLHA_user_normal|else return new Cached_OLHA_user_normal|' src/cached_OLHA.cpp

# Update to detect aarch64 and ppc64le
rm -f ./config.{sub,guess}
%get_config_sub ./config.sub
%get_config_guess ./config.guess
chmod +x ./config.{sub,guess}

./configure --prefix=%i --with-QDpath=$QD_ROOT CXXFLAGS="-Wno-deprecated -I$OPENSSL_ROOT/include" LDFLAGS="-L$OPENSSL_ROOT/lib"
# The following hack insures that the bins with the library linked explicitly
# rather than indirectly, as required by the gold linker
%build
make %{makeprocesses}
%install
make install

%post
%{relocateConfig}lib/blackhat/lib*.la
%{relocateConfig}bin/blackhat-config
%{relocateConfig}bin/dataInstall
