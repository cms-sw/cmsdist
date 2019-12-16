### RPM external bazel 0.26.1

Source: https://github.com/bazelbuild/bazel/releases/download/%{realversion}/bazel-%{realversion}-dist.zip
BuildRequires: java-env
%prep

%define __unzip unzip -d bazel-%{realversion}

%setup -q -n bazel-%{realversion}

%build

# For some build steps, bazel uses a process-wrapper that is executed in an empty environment.
# Therefore, the wrapper is linked to the system library /lib64/libstdc++.so.6, and complains about
# a missing GLIBCXX_3.4.21 version when (e.g.) used during the compilation of tensorflow python
# modules invoked via swig. This mechanism of bazel is actually only useful in combination with its
# remote compilation features. When disabling the process-wrapper, the local environment is taken
# into account which is the desired behavior for us. For example, see:
#   - https://github.com/bazelbuild/bazel/issues/4137
#   - https://github.com/bazelbuild/bazel/issues/4510
#   - https://github.com/tensorflow/tensorboard/issues/1611
# The sed command below changes the line:
# https://github.com/bazelbuild/bazel/blob/0.26.1/src/main/java/com/google/devtools/build/lib/exec/local/LocalSpawnRunner.java#L115
sed -i 's/this.useProcessWrapper = useProcessWrapper;/this.useProcessWrapper = false;/g' src/main/java/com/google/devtools/build/lib/exec/local/LocalSpawnRunner.java
export EXTRA_BAZEL_ARGS="--host_javabase=@local_jdk//:jdk"
bash ./compile.sh

%install
mkdir %{i}/bin
cp output/bazel %{i}/bin/.
