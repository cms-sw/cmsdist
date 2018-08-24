### RPM external bazel 0.16.1

Source: https://github.com/bazelbuild/bazel/releases/download/%{realversion}/bazel-%{realversion}-dist.zip
BuildRequires: java-env
%prep

%define __unzip unzip -d bazel-%{realversion}

%setup -q -n bazel-%{realversion}

%build
bash ./compile.sh

%install
mkdir %{i}/bin
cp output/bazel %{i}/bin/.


