### RPM external py2-psutil 5.4.5
## IMPORT build-with-pip

%define find %i -name '*.egg-info' -delete; \
    find %i -name '.package-checksum' -delete
