### RPM virtual openssl-virtual 0.9.7a
Source: none
Provides: config(openssl) 
Provides: libcrypto.so.4  
Provides: libssl.so.4  
Provides: openssl 
%prep
%build
%install
echo 'This is only a virtual package, please install your distribution openssl.rpm or equivalent'> %{i}/README 
