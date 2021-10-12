### RPM external py2-htcondor 9.2.0
## IMPORT build-with-pip

Provides: libcrypto-b8807daa.so.1.1(OPENSSL_1_1_0)(64bit)
Provides: libcrypto-b8807daa.so.1.1(OPENSSL_1_1_0d)(64bit)
Provides: libcrypto-b8807daa.so.1.1(OPENSSL_1_1_0f)(64bit)
Provides: libcrypto-b8807daa.so.1.1(OPENSSL_1_1_0i)(64bit)
Provides: libcrypto-b8807daa.so.1.1(OPENSSL_1_1_1)(64bit)
Provides: libglobus_gssapi_gsi-46531449.so.4.10.9(globus_gssapi_gsi)(64bit)
Provides: libgomp-3300acd3.so.1.0.0(GOMP_1.0)(64bit)
Provides: libgomp-3300acd3.so.1.0.0(OMP_1.0)(64bit)
Provides: libk5crypto-622ef25b.so.3.1(k5crypto_3_MIT)(64bit)
Provides: libkeyutils-1-ff31573b.2.so(KEYUTILS_0.3)(64bit)
Provides: libkrb5-fb0d2caa.so.3.3(krb5_3_MIT)(64bit)
Provides: libkrb5support-d7ce89d4.so.0.1(krb5support_0_MIT)(64bit)
Provides: libssl-6536aedd.so.1.1(OPENSSL_1_1_0)(64bit)

%define PipDownloadSourceType none

%define PipPostBuild perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/*
