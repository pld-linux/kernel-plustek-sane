#
# Conditional build:
%bcond_without	dist_kernel	# without distribution kernel
#
Summary:	Plustek scanner kernel module
Summary(pl.UTF-8):   Moduł jądra dla skanerów Plustek
Name:		kernel-plustek-sane
%define	bver	0.45
%define	sver	5
Version:	%{bver}.%{sver}
%define	_rel	4.x
Release:	%{_rel}
License:	BSD
Group:		Base/Kernel
Source0:	http://www.gjaeger.de/scanner/current/plustek-sane-%{bver}-%{sver}.tar.gz
# Source0-md5:	ca8f7b1f7ee35b3c09caf0cb16dc6b88
Patch0:		%{name}-Makefile.patch
Patch1:		%{name}-alpha.patch
Patch2:		%{name}-inline-in-header.patch
URL:		http://www.gjaeger.de/scanner/plustek.html
%{?with_dist_kernel:BuildRequires:	kernel-headers}
#BuildRequires:	%{kgcc_package}
BuildRequires:	rpmbuild(macros) >= 1.118
ExcludeArch:	sparc sparcv9 sparc64
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package contains kernel module which drives Plustek scanners.

%description -l pl.UTF-8
Pakiet zawiera moduł jądra sterujący skanerami Plustek.

%package -n kernel-char-plustek
Summary:	Plustek scanner kernel module
Summary(pl.UTF-8):   Moduł jądra dla skanerów Plustek
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel_up}
Requires(post,postun):	/sbin/depmod
Requires:	sane-backends >= 1.0.7
Requires:	sane-backends-plustek >= 1.0.7

%description -n kernel-char-plustek
This package contains kernel module which drives Plustek scanners.

%description -n kernel-char-plustek -l pl.UTF-8
Pakiet zawiera moduł jądra sterujący skanerami Plustek.

%package -n kernel-smp-char-plustek
Summary:	Plustek scanner kernel SMP module
Summary(pl.UTF-8):   Moduł jądra SMP dla skanerów Plustek
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel_smp}
Requires(post,postun):	/sbin/depmod
Requires:	sane-backends >= 1.0.7
Requires:	sane-backends-plustek >= 1.0.7

%description -n kernel-smp-char-plustek
This package contains kernel SMP module which drives Plustek scanners.

%description -n kernel-smp-char-plustek -l pl.UTF-8
Pakiet zawiera moduł jądra SMP sterujący skanerami Plustek.

%prep
%setup -q -c
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
cd backend/plustek_driver/src
## generate new makefile
echo "obj-m := pt_drv.o" >Makefile
echo "pt_drv-objs := dac.o detect.o genericio.o image.o map.o misc.o models.o" \
	"io.o procfs.o motor.o p9636.o ptdrv.o scale.o tpa.o p48xx.o p12.o" \
	"p12ccd.o" >> Makefile
echo "CFLAGS += -D_PTDRV_V1=0 -D_PTDRV_V0=42 -D_PTDRV_BUILD=10" >> Makefile
cp ../h/*.h .
cp ../../plustek-share.h .
# kernel module(s)
for cfg in %{?with_dist_kernel:%{?with_smp:smp} up}%{!?with_dist_kernel:nondist}; do
	if [ ! -r "%{_kernelsrcdir}/config-$cfg" ]; then
		exit 1
	fi
	rm -rf include
	install -d include/{linux,config}
	ln -sf %{_kernelsrcdir}/config-$cfg .config
	ln -sf %{_kernelsrcdir}/include/linux/autoconf-$cfg.h include/linux/autoconf.h
	ln -sf %{_kernelsrcdir}/include/asm-%{_target_base_arch} include/asm
	ln -sf %{_kernelsrcdir}/Module.symvers-$cfg Module.symvers
	touch include/config/MARKER

	%{__make} -C %{_kernelsrcdir} clean \
		RCS_FIND_IGNORE="-name '*.ko' -o" \
		M=$PWD O=$PWD \
		%{?with_verbose:V=1}
	%{__make} -C %{_kernelsrcdir} modules \
		CC="%{__cc}" \
		M=$PWD O=$PWD \
		%{?with_verbose:V=1}
	mv iscsi_sfnet{,-$cfg}.ko
done
cd ..

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc
install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/misc

install backend/plustek_driver/pt_drv.o.smp	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/misc/pt_drv.o
install backend/plustek_driver/pt_drv.o		$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc

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
