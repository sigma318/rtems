#
# spec file for autoconf 
#

%define rpmvers 2.52
%define srcvers	2.52

%define _defaultbuildroot	/var/tmp/%{name}-%{srcvers}-root
%define _prefix			/opt/rtems
%define _name			autoconf

%if "%{_prefix}" != "/usr"
%define name			%{_name}-rtems
%define _infodir		%{_prefix}/info
%define _mandir			%{_prefix}/man
%else
%define name			%{_name}
%endif


Vendor:       http://www.rtems.com
Name:         %{name}
Packager:     Ralf Corsepius <corsepiu@faw.uni-ulm.de>

Copyright:    GPL
URL:          http://www.gnu.org/software/autoconf
Group:        rtems
Provides:     autoconf
Autoreqprov:  on
Version:      %{rpmvers}
Release:      0
Summary:      Tool for automatically generating GNU style Makefile.in's
BuildArch:    noarch
BuildRoot:    %{_defaultbuildroot}
BuildPreReq:  autoconf perl m4 gawk
PreReq:       /sbin/install-info

Source: autoconf-%{srcvers}.tar.bz2

%description
GNU's Autoconf is a tool for configuring source code and Makefiles.
Using Autoconf, programmers can create portable and configurable
packages, since the person building the package is allowed to
specify various configuration options.
You should install Autoconf if you are developing software and you'd
like to use it to create shell scripts which will configure your
source code packages.
Note that the Autoconf package is not required for the end user who
may be configuring software with an Autoconf-generated script;
Autoconf is only required for the generation of the scripts, not
their use.

%prep
%setup -q -n %{_name}-%{srcvers}

%build
./configure --prefix=%{_prefix} --infodir=%{_infodir} --mandir=%{_mandir}
make

%install
%makeinstall
gzip -9qf $RPM_BUILD_ROOT%{_infodir}/autoconf.info* 2>/dev/null
# RTEMS's standards.info comes from binutils
rm -f $RPM_BUILD_ROOT%{_infodir}/standards.info*
# gzip -9qf $RPM_BUILD_ROOT%{_infodir}/standards.info* 2>/dev/null
gzip -9qf $RPM_BUILD_ROOT%{_mandir}/man?/* 2>/dev/null

%clean
[ x"$RPM_BUILD_ROOT" = x"%{_defaultbuildroot}" ] ; \
   rm -rf "$RPM_BUILD_ROOT"

%post
install-info  --info-dir=%{_infodir} %{_infodir}/autoconf.info.gz
#install-info  --info-dir=%{_infodir} %{_infodir}/standards.info.gz

%preun
if [ $1 = 0 ]; then
  install-info --delete --info-dir=%{_infodir} %{_infodir}/autoconf.info.gz
#  install-info --delete --info-dir=%{_infodir} %{_infodir}/standards.info.gz
fi   

%files
%defattr(-,root,root)
%doc AUTHORS COPYING ChangeLog NEWS README THANKS
%{_bindir}/*
%doc %{_infodir}/autoconf.info*.gz
#%doc %{_infodir}/standards.info*.gz
%doc %{_mandir}/man?/*.gz
%{_datadir}/autoconf
