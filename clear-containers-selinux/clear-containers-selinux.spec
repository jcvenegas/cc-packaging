%global selinuxtype	targeted
%global moduletype	services
%global modulenames	cc-proxy
 
# Usage: _format var format
#   Expand 'modulenames' into various formats as needed
#   Format must contain '$x' somewhere to do anything useful
%global _format() export %1=""; for x in %{modulenames}; do %1+=%2; %1+=" "; done;
 
# Relabel files
%global relabel_files() \ # ADD files in *.fc file
 
 
# Version of distribution SELinux policy package 
%global selinux_policyver_rhel 3.13.1-102.el7
%global selinux_policyver 3.13.1-128.6.fc22

# Version of Python for f25
%global fedora25_pythonver 2.7.12-7.fc25
 
# Package information
Name:			clear-containers-selinux
Version:		0.1
Release:		5.<B_CNT>
License:		GPLv2
Group:			System Environment/Base
Summary:		SELinux Policies for Clear Containers
BuildArch:		noarch
URL:			https://github.com/01org/cc-oci-runtime
%if 0%{?rhel} >= 7
Requires(post):		selinux-policy-base >= %{selinux_policyver_rhel}, selinux-policy-targeted >= %{selinux_policyver_rhel}, policycoreutils, policycoreutils-python libselinux-utils
%else
Requires(post):		selinux-policy-base >= %{selinux_policyver}, selinux-policy-targeted >= %{selinux_policyver}, policycoreutils, policycoreutils-python libselinux-utils
%endif
%if 0%{?fedora} >= 25
BuildRequires:         python >= %{fedora25_pythonver}
%endif
BuildRequires:		selinux-policy selinux-policy-devel
 
Source:			%{name}-%{version}.tar.gz
 
%description
SELinux policy modules for use with Clear Containers
 
%prep
%setup -q
 
%build
make SHARE="%{_datadir}" TARGETS="%{modulenames}"
 
%install
 
# Install policy modules
%_format MODULES $x.pp.bz2
install -d %{buildroot}%{_datadir}/selinux/packages
install -m 0644 $MODULES \
	%{buildroot}%{_datadir}/selinux/packages
 
%post
#
# Install all modules in a single transaction
#
%_format MODULES %{_datadir}/selinux/packages/$x.pp.bz2
%{_sbindir}/semodule -n -s %{selinuxtype} -i $MODULES
if %{_sbindir}/selinuxenabled ; then
    %{_sbindir}/load_policy
    %relabel_files
fi
 
 
%postun
if [ $1 -eq 0 ]; then
	%{_sbindir}/semodule -n -r %{modulenames} &> /dev/null || :
	if %{_sbindir}/selinuxenabled ; then
		%{_sbindir}/load_policy
		%relabel_files
	fi
fi
 
%files
%defattr(-,root,root,0755)
%attr(0644,root,root) %{_datadir}/selinux/packages/*.pp.bz2
 
%changelog
* Tue Jan 24 2017 Geronimo Orozco <geronimo.orozco@intel.com> - 0.1-1
- First Build
