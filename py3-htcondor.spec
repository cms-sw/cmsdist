### RPM external py3-htcondor 10.2.3
## IMPORT build-with-pip3

# dependencies required by 8.9.7
#Provides: libcrypto-d47fc050.so.1.1(OPENSSL_1_1_0)(64bit)
#Provides: libcrypto-d47fc050.so.1.1(OPENSSL_1_1_0d)(64bit)
#Provides: libcrypto-d47fc050.so.1.1(OPENSSL_1_1_0f)(64bit)
#Provides: libcrypto-d47fc050.so.1.1(OPENSSL_1_1_0i)(64bit)
#Provides: libcrypto-d47fc050.so.1.1(OPENSSL_1_1_1)(64bit)

# dependencies required by 9.2.0
#Provides: libglobus_gssapi_gsi-46531449.so.4.10.9(globus_gssapi_gsi)(64bit)
#Provides: libgomp-3300acd3.so.1.0.0(GOMP_1.0)(64bit)
#Provides: libgomp-3300acd3.so.1.0.0(OMP_1.0)(64bit)
#Provides: libk5crypto-622ef25b.so.3.1(k5crypto_3_MIT)(64bit)
#Provides: libkeyutils-1-ff31573b.2.so(KEYUTILS_0.3)(64bit)
#Provides: libkrb5-fb0d2caa.so.3.3(krb5_3_MIT)(64bit)
#Provides: libkrb5support-d7ce89d4.so.0.1(krb5support_0_MIT)(64bit)
#Provides: libssl-6536aedd.so.1.1(OPENSSL_1_1_0)(64bit)

# dependencies required by 10.2.3
Provides: libcrypto-19957f5b.so.1.0.2k(OPENSSL_1.0.1_EC)(64bit)
Provides: libcrypto-19957f5b.so.1.0.2k(libcrypto.so.10)(64bit)
Provides: libgomp-a34b3233.so.1.0.0(GOMP_4.0)(64bit)
Provides: libgomp-a34b3233.so.1.0.0(OMP_1.0)(64bit)
Provides: libk5crypto-b1f99d5c.so.3.1(k5crypto_3_MIT)(64bit)
Provides: libkeyutils-dfe70bd6.so.1.5(KEYUTILS_0.3)(64bit)
Provides: libkeyutils-dfe70bd6.so.1.5(KEYUTILS_1.0)(64bit)
Provides: libkeyutils-dfe70bd6.so.1.5(KEYUTILS_1.5)(64bit)
Provides: libkrb5-fcafa220.so.3.3(krb5_3_MIT)(64bit)
Provides: libkrb5support-d0bcff84.so.0.1(krb5support_0_MIT)(64bit)
Provides: libssl-2a9eae6f.so.1.0.2k(libssl.so.10)(64bit)
Provides: libuuid-f64cda11.so.1.3.0(UUID_1.0)(64bit)

%define PipDownloadSourceType none

%define PipPostBuild perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/*
