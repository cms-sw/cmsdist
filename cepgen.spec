### RPM external cepgen 1.0.1

%define tag 8bb7a41787b4efb2b765e1de5d39da6bce6a2b25
%define branch %{realversion}
%define github_user cepgen
Source: git+https://github.com/%github_user/%{n}.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz

BuildRequires: cmake ninja

%prep
%setup -n %{n}-%{realversion}

%build
rm -rf ../build
mkdir ../build
cd ../build

cmake ../%{n}-%{realversion} \
  -G Ninja \
  -DCMAKE_INSTALL_PREFIX:PATH="%i" \
  -DCMAKE_BUILD_TYPE=Release

ninja -v %{makeprocesses}

%install
cd ../build
ninja %{makeprocesses} install

case $(uname) in Darwin ) so=dylib ;; * ) so=so ;; esac
rm -f %i/lib/libCepGen-[A-Z]*-%realversion.$so

%post
%{relocateConfig}bin/cepgen
