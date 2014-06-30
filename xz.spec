### RPM external xz 5.0.3__5.1.2alpha
%define generic_version 5.0.3
%define fcarm_version 5.1.2alpha
%define mic %(case %cmsplatf in (*_mic_*) echo true;; (*) echo false;; esac)
%if "%mic" == "true"
Requires: icc
%endif
Source0: http://tukaani.org/%{n}/%{n}-%{generic_version}.tar.gz
Source1: http://tukaani.org/%{n}/%{n}-%{fcarm_version}.tar.gz

%define isfcarm %(case %{cmsplatf} in (fc*_arm*) echo 1 ;; (*) echo 0 ;; esac)
Source0: git+https://github.com/%github_user/xz.git?obj=%{branch}/%{tag}&export=%{n}-%{generic_version}&output=/%{n}-%{generic_version}.tgz
Source1: git+https://github.com/%github_user/xz.git?obj=%{armbranch}/%{armtag}&export=%{n}-%{fcarm_version}&output=/%{n}-%{fcarm_version}.tgz

BuildRequires: autotools

%prep
%if %isfcarm
%setup -b 1 -n %{n}-%{fcarm_version}
%else
%setup -b 0 -n %{n}-%{generic_version}
%endif

%build
case %{cmsplatf} in
   *_mic_* )
    CXX="icpc -fPIC -mmic"  CC="icc -fPIC -mmic" ./configure CFLAGS='-fPIC -Ofast' --prefix=%i --disable-static --host=x86_64-k1om-linux
     ;;
   * )
     ./configure CFLAGS='-fPIC -Ofast' --prefix=%i --disable-static
     ;;
esac
make %{makeprocesses}

%install
make %{makeprocesses} install

%define strip_files %{i}/lib
%define drop_files %{i}/share
