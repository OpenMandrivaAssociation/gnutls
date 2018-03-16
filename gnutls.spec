%define url_ver %(echo %{version}|cut -d. -f1,2)
%define dirver %(echo %{version}|cut -d. -f1,2,3)
%define _disable_rebuild_configure 1

%define major 30
%define xxmajor 28
%define sslmajor 27
%define libname %mklibname %{name} %{major}
%define libnamexx %mklibname %{name}xx %{xxmajor}
%define libssl %mklibname %{name}-openssl %{sslmajor}
%define devname %mklibname %{name} -d

Summary:	Library providing a secure layer (SSL)
Name:		gnutls
Version:	3.6.2
Release:	2
License:	GPLv2+ and LGPLv2+
Group:		System/Libraries
Url:		http://www.gnutls.org
Source0:	ftp://ftp.gnutls.org/gcrypt/gnutls/v%{url_ver}/%{name}-%{version}.tar.xz
Patch1:		gnutls-3.2.7-rpath.patch
Patch2:		gnutls-3.6.0-clang.patch
# Use only FIPS approved ciphers in the FIPS mode
Patch7:		gnutls-2.12.21-fips-algorithms.patch

BuildRequires:	libunistring-devel
BuildRequires:	lzo-devel
BuildRequires:	pkgconfig(libgcrypt)
BuildRequires:	pkgconfig(libtasn1)
BuildRequires:	pkgconfig(p11-kit-1)
BuildRequires:	pkgconfig(nettle)
BuildRequires:	pkgconfig(libidn)
%ifnarch %{arm} %{mips} aarch64
BuildRequires:	valgrind
%endif

%description
GnuTLS is a project that aims to develop a library which provides 
a secure layer, over a reliable transport layer.

%package -n	%{libname}
Summary:	Library providing a secure layer (SSL)
Group:		System/Libraries
Suggests:	%{name}-locales = %{version}-%{release}
%if "%{_lib}" == "lib64"
Conflicts:	lib%{name}%{major} < %{version}
%endif

%description -n	%{libname}
This package contains a shared library for %{name}.

%package -n	%{libnamexx}
Summary:	Library providing a secure layer (SSL)
Group:		System/Libraries
Conflicts:	%{_lib}gnutls28 < 3.1.9.1-3

%description -n	%{libnamexx}
This package contains a shared library for %{name}.

%package -n	%{libssl}
Summary:	Library providing a secure layer (SSL)
Group:		System/Libraries
Obsoletes:	%{_lib}gnutls-ssl27 < 3.1.9.1-3

%description -n	%{libssl}
This package contains a shared library for %{name}.

%package -n	%{devname}
Summary:	Development files for %{name}
Group:		Development/C
Requires:	%{name} = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}
Requires:	%{libnamexx} = %{version}-%{release}
Requires:	%{libssl} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n	%{devname}
This package contains all necessary files to compile or develop
programs/libraries that use %{name}.

%package locales
Summary:	Locale files for GnuTLS
Group:		System/Internationalization 
BuildArch:	noarch
Conflicts:	%{mklibname gnutls 28} <= 3.1.9.1-1

%description locales
Locale files for GnuTLS main library.

%prep
%setup -qn %{name}-%{dirver}
%patch1 -p1 -b .rpath~
%patch2 -p1 -b .clang~
# This patch is not applicable as we use nettle now but some parts will be
# later reused.
#%patch7 -p1 -b .fips~

sed 's/gnutls_srp.c//g' -i lib/Makefile.in
sed 's/gnutls_srp.lo//g' -i lib/Makefile.in


%build
%configure \
	--with-included-libtasn1=no \
	--disable-srp-authentication \
	--with-libz-prefix=%{_prefix} \
	--enable-openssl-compatibility \
%ifnarch %{arm} %{mips} aarch64
	--enable-valgrind-tests \
%endif
	--disable-non-suiteb-curves \
	--disable-rpath \
	--disable-guile

%make

%check
#make check

%install
%makeinstall_std

%find_lang %{name}

%files
%doc NEWS README.md
%{_bindir}/[cgs]*
%{_bindir}/psktool
%{_bindir}/p11tool
%{_bindir}/ocsptool
%{_mandir}/man?/*
%{_infodir}/*

%files locales -f %{name}.lang

%files -n %{libname}
%{_libdir}/libgnutls.so.%{major}*

%files -n %{libnamexx}
%{_libdir}/libgnutlsxx.so.%{xxmajor}*

%files -n %{libssl}
%{_libdir}/libgnutls-openssl.so.%{sslmajor}*

%files -n %{devname}
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/gnutls
