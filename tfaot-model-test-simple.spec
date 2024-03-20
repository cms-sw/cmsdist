### RPM external tfaot-model-test-simple 1.0.0

%define tool_name tfaot-model-test-simple

%define github_user riga
%define tag ac5e4ed8507ad63be5814247ef32cb9d0ecc21ff
%define branch dev
Source: git+https://github.com/%{github_user}/cms-tf-aot.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz

%define aot_config test_models/simple/aot_config.yaml

## INCLUDE tfaot-compile
