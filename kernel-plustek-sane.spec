#
# Conditional build:
# _without_dist_kernel	- without distribution kernel
#
Summary:	Plustek scanner kernel module
Summary(pl):	Modu³ j±dra dla skanerów Plustek
Name:		kernel-plustek-sane
%define	bver	0.45
%define	sver	5
Version:	%{bver}.%{sver}
%define	_rel	1
Release:	%{_rel}
License:	BSD
Group:		Base/Kernel
Source0:	http://www.gjaeger.de/scanner/current/plustek-sane-%{bver}-%{sver}.tar.gz
# Source0-md5:	ca8f7b1f7ee35b3c09caf0cb16dc6b88
Patch0:		%{name}-Makefile.patch
Patch1:		%{name}-alpha.patch
URL:		http://www.gjaeger.de/scanner/plustek.html
%{!?_without_dist_kernel:BuildRequires:         kernel-headers}
BuildRequires:	%{kgcc_package}
ExcludeArch:	sparc sparcv9 sparc64
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package contains kernel module which drives Plustek scanners.

%description -l pl
Pakiet zawiera modu³ j±dra steruj±cy skanerami Plustek.

%package -n kernel-char-plustek
Summary:	Plustek scanner kernel module
Summary(pl):	Modu³ j±dra dla skanerów Plustek
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{!?_without_dist_kernel:%requires_releq_kernel_up}
Requires(post,postun):	/sbin/depmod
Requires:	sane-backends >= 1.0.7
Requires:	sane-backends-plustek >= 1.0.7

%description -n kernel-char-plustek
This package contains kernel module which drives Plustek scanners.

%description -n kernel-char-plustek -l pl
Pakiet zawiera modu³ j±dra steruj±cy skanerami Plustek.

%package -n kernel-smp-char-plustek
Summary:	Plustek scanner kernel SMP module
Summary(pl):	Modu³ j±dra SMP dla skanerów Plustek
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{!?_without_dist_kernel:%requires_releq_kernel_smp}
Requires(post,postun):	/sbin/depmod
Requires:	sane-backends >= 1.0.7
Requires:	sane-backends-plustek >= 1.0.7

%description -n kernel-smp-char-plustek
This package contains kernel SMP module which drives Plustek scanners.

%description -n kernel-smp-char-plustek -l pl
Pakiet zawiera modu³ j±dra SMP steruj±cy skanerami Plustek.

%prep
%setup -q -c
%patch0 -p1
%patch1 -p1

%build
cd backend/plustek_driver
%{__make} all BUILD_SMP=1 OPT_FLAGS="%{rpmcflags}"
mv -f pt_drv.o{,.smp}
%{__make} clean
%{__make} all OPT_FLAGS="%{rpmcflags}" CC=%{kgcc}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc
install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/misc

install  backend/plustek_driver/pt_drv.o.smp	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/misc/pt_drv.o
install  backend/plustek_driver/pt_drv.o	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc

%clean 
rm -rf $RPM_BUILD_ROOT

%post	-n kernel-char-plustek
%depmod %{_kernel_ver}

%postun	-n kernel-char-plustek
%depmod %{_kernel_ver}

%post	-n kernel-smp-char-plustek
%depmod %{_kernel_ver}smp

%postun	-n kernel-smp-char-plustek
%depmod %{_kernel_ver}smp

%files -n kernel-char-plustek
%defattr(644,root,root,755)
%doc backend/plustek_driver/{ChangeLog,FAQ,INSTALL,README,TODO}
%lang(de) %doc backend/plustek_driver/INSTALL.GER
/lib/modules/%{_kernel_ver}/misc/*

%files -n kernel-smp-char-plustek
%defattr(644,root,root,755)
%doc backend/plustek_driver/{ChangeLog,FAQ,INSTALL,README,TODO}
%lang(de) %doc backend/plustek_driver/INSTALL.GER
/lib/modules/%{_kernel_ver}smp/misc/*
