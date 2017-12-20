### RPM external mcfm 6.3

%define keep_archives true
%define tag d2e025ce8044976b95811b1a92e802f5e4eeb5ae
%define branch cms/%{realversion}
%define github_user cms-externals
Source: git+https://github.com/%github_user/%{n}.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz

Requires: root

%prep
%setup -q -n %{n}-%{realversion}

%build
mkdir -p obj
pushd QCDLoop
make
popd
make

mv %_builddir/%{n}-%{realversion}/Bin %_builddir/%{n}-%{realversion}/bin

mkdir -p %_builddir/%{n}-%{realversion}/lib
ar cr %_builddir/%{n}-%{realversion}/lib/libMCFM.a %_builddir/%{n}-%{realversion}/obj/*.o

%install

rm %_builddir/%{n}-%{realversion}/bin/mcfm

cp -r %_builddir/%{n}-%{realversion}/lib %{i}
cp -r %_builddir/%{n}-%{realversion}/bin %{i}

%post
