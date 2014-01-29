### RPM virtual krb5-virtual libs
Source: none
Provides: config(krb5-libs) 
Provides: libcom_err.so.3  
Provides: libdes425.so.3  
Provides: libdyn.so.1  
Provides: libgssapi_krb5.so.2  
Provides: libgssrpc.so.3  
Provides: libk5crypto.so.3  
Provides: libkadm5clnt.so.5  
Provides: libkadm5srv.so.5  
Provides: libkdb5.so.3  
Provides: libkrb4.so.2  
Provides: libkrb5.so.3  
Provides: libpty.so.1  
Provides: krb5-libs 
%prep
%build
%install
echo 'This is only a virtual package, please install your distribution libkrb5-libs.rpm or equivalent'> %{i}/README 
