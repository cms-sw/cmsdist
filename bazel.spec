### RPM external bazel 3.7.2

Source: https://github.com/bazelbuild/bazel/releases/download/%{realversion}/bazel-%{realversion}-dist.zip

BuildRequires: java-env python3 python-python3

# For some build steps, bazel uses a process-wrapper that is executed in an empty environment.
# Therefore, the wrapper is linked to the system library /lib64/libstdc++.so.6, and complains about
# a missing GLIBCXX_3.4.21 version when (e.g.) used during the compilation of tensorflow python
# modules invoked via swig. This mechanism of bazel is actually only useful in combination with its
# remote compilation features. When disabling the process-wrapper, the local environment is taken
# into account which is the desired behavior for us. For example, see:
#   - https://github.com/bazelbuild/bazel/issues/4137
#   - https://github.com/bazelbuild/bazel/issues/4510
#   - https://github.com/tensorflow/tensorboard/issues/1611

# configuration issue
# https://github.com/bazelbuild/bazel/issues/9392
Patch0: bazel-3.7.0-patches
Patch1: bazel-3.7.2-gcc11

%prep
%setup -q -c -n bazel-%{realversion}

%patch0 -p1
%patch1 -p1

%build

export EXTRA_BAZEL_ARGS="--host_javabase=@local_jdk//:jdk --jobs %{compiling_processes}"
bash ./compile.sh

%install
mkdir %{i}/bin
cp output/bazel %{i}/bin/.
