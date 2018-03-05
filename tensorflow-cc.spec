### RPM external tensorflow-cc 1.5.0

Source: none

BuildRequires: tensorflow-sources

%prep

%build


%install

tar xfz ${TENSORFLOW_SOURCES_ROOT}/libtensorflow_cc.tar.gz -C %{i}

