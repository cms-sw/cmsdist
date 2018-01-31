### RPM external bazel 0.9.0

Source: https://github.com/bazelbuild/bazel/releases/download/%{realversion}/bazel-%{realversion}-dist.zip
BuildRequires: java-env
Patch1: bazel-java-vm
Patch2: bazel-0.9.0-860af5b
%prep

%define __unzip unzip -d bazel-%{realversion}

%setup -q -n %{n}-%{realversion}
%patch1 -p1
%patch2 -p1

%build
bash ./compile.sh

%install
mkdir %{i}/bin
cp output/bazel %{i}/bin/.


