### RPM external bloom-filter 1.0
## NOCOMPILER

%define source0 https://www.partow.net/downloads/bloom_filter.zip
%define source_prefix bloom_filter
Source: %{source0}

%prep
%setup -n %{source_prefix}

%build
mkdir ../include
mkdir ../shared
cp -v *.hpp ../include
cp -v * ../shared

%install
cp -rv ../include %{i}
cp -rv ../shared %{i}
%post
