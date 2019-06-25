### RPM external xxHash 0.7.0
## INITENV SETV XXHASH_SOURCE %{source0}
## INITENV SETV XXHASH_STRIP_PREFIX %{source_prefix}

%define tag 434b5a425bc7c8f6892d352cd8c4dd93c34d10b0
%define branch cms/master/244afa1
%define github_user cms-sw

%define source0 https://github.com/Cyan4973/xxHash/archive/v0.7.0.tar.gz
%define source_prefix %{n}-%{realversion}
Source: %{source0}

BuildRequires: gmake cmake

%prep
%setup -n %{source_prefix}

%build
# Update to get AArch64

rm -f ./config.{sub,guess}
curl -L -k -s -o ./config.sub 'http://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.sub;hb=HEAD'
curl -L -k -s -o ./config.guess 'http://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.guess;hb=HEAD'
chmod +x ./config.{sub,guess}

cmake cmake_unofficial \
 -DCMAKE_INSTALL_PREFIX:PATH=%{i}

make %{makeprocesses}

%install

make install

