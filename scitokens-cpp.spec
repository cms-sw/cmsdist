### RPM external scitokens-cpp 0.6.3
Source: https://github.com/scitokens/scitokens-cpp/releases/download/v%{realversion}/%{n}-%{realversion}.tar.gz

BuildRequires: cmake libuuid

%setup -n %{n}-%{realversion}

%build
rm -rf ../build; mkdir ../build; cd ../build
cmake ../%{n}-%{realversion} \
  -DCMAKE_INSTALL_PREFIX=%{i} \
  -DCMAKE_BUILD_TYPE=Release
  
%install
cd ../build
make %{makeprocesses}
make install
