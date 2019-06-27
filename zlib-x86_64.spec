### RPM external zlib-x86_64 1.2.11
%define git_repo cms-externals
%define git_branch cms/v1.2.11
%define git_commit 822f7f5a8c57802faf8bbfe16266be02eff8c2e2
Source0: git://github.com/%{git_repo}/zlib.git?obj=%{git_branch}/%{git_commit}&export=zlib-%{realversion}&output=/zlib-%{realversion}.tgz

## IMPORT zlib-build
# bla bla
