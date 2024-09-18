### RPM external libjpeg-turbo 3.0.4
## INITENV +PATH LD_LIBRARY_PATH %{i}/lib64
Source: https://github.com/libjpeg-turbo/libjpeg-turbo/archive/refs/tags/%{realversion}.tar.gz

BuildRequires: nasm autotools gmake cmake

%prep
%setup -n %{n}-%{realversion}

%build
# Update to get AArch64

rm -f ./config.{sub,guess}
%get_config_sub ./config.sub
%get_config_guess ./config.guess
chmod +x ./config.{sub,guess}

cmake -DCMAKE_INSTALL_PREFIX=%{i} -DENABLE_SHARED=TRUE -DENABLE_STATIC=FALSE -DWITH_JPEG8=TRUE

make %{makeprocesses}
%install
make install

%define strip_files %{i}/lib
%define drop_files %{i}/{share,man}

%post
%relocateConfigAll lib64/pkgconfig lib*.pc
