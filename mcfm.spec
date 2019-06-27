### RPM external mcfm 6.3

%define keep_archives true
%define tag d2e025ce8044976b95811b1a92e802f5e4eeb5ae
%define branch cms/%{realversion}
%define github_user cms-externals
Source: git+https://github.com/%github_user/%{n}.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz

%define isaarch64 %(case %{cmsplatf} in (*_aarch64_*) echo 1 ;; (*) echo 0 ;; esac)

Patch0: mcfm-6.3-opt-for-size

Requires: root

%prep
%setup -q -n %{n}-%{realversion}

# This patch is needed as workaround for GCC PR63304
# https://gcc.gnu.org/bugzilla/show_bug.cgi?id=63304
%if 0%{isaarch64}
%patch0 -p1
%endif

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
# bla bla
