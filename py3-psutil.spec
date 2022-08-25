### RPM external py3-psutil 5.9.1
## IMPORT build-with-pip3

%define find %i -name '*.egg-info' -delete; \
    find %i -name '.package-checksum' -delete
