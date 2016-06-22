### RPM external tinyxml 2.5.3
%define tag 3b1ed8542a820e77de84bc08734bde904c3b12be
%define branch cms/2.5.3
%define github_user cms-externals
Source: git+https://github.com/%github_user/%{n}.git?obj=%{branch}/%{tag}&export=%{n}.%{realversion}&output=/%{n}.%{realversion}-%{tag}.tgz

BuildRequires: gmake
Requires: boost

%prep
%setup -n %{n}.%{realversion}

%build
export BOOST_ROOT

gmake

%install

mkdir %{i}/{lib,include}

so=so
case $(uname) in
  Darwin )
    so=dylib
    ;;
esac
cp libtinyxml.$so %{i}/lib/
cp *.h %{i}/include/
