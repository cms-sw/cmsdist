### RPM external heppdt 3.03.00
%define tag ad5bd2d96ca39491a5c0f729c9ebbec9a36b85bf
%define branch cms/3.03.00
%define github_user cms-externals
Source: git+https://github.com/%{github_user}/heppdt.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}-%{tag}.tgz

%define keep_archives yes

Requires: tbb

%if "%{?cms_cxx:set}" != "set"
%define cms_cxx g++
%endif

%if "%{?cms_cxxflags:set}" != "set"
%define cms_cxxflags -O2 -std=c++14
%endif

%prep
%setup -q -n heppdt-%{realversion}

# Update to detect aarch64 and ppc64le
rm -f ./config.{sub,guess}
%get_config_sub ./config.sub
%get_config_guess ./config.guess
chmod +x ./config.{sub,guess}

CXX="%cms_cxx" CXXFLAGS="%cms_cxxflags" CPPFLAGS="-I$TBB_ROOT/include" LDFLAGS="-L$TBB_ROOT/lib -ltbb" ./configure  --prefix=%{i} 

%build
make 

%install
make install
