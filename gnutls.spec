%define url_ver %(echo %{version}|cut -d. -f1,2)
%define dirver %(echo %{version}|cut -d. -f1,2,3)

%define major 28
%define sslmajor 27
%define xsslmajor 0
%define libname %mklibname %{name} %{major}
%define libnamexx %mklibname %{name}xx %{major}
%define libssl %mklibname %{name}-openssl %{sslmajor}
%define libxssl %mklibname %{name}-xssl %{xsslmajor}
%define devname %mklibname %{name} -d

Summary:	Library providing a secure layer (SSL)
Name:		gnutls
Version:	3.2.13
Release:	1
License:	GPLv2+ and LGPLv2+
Group:		System/Libraries
Url:		http://www.gnutls.org
Source0:	ftp://ftp.gnutls.org/gcrypt/gnutls/v%{url_ver}/%{name}-%{version}.tar.xz
Patch1:		gnutls-3.2.7-rpath.patch
# Use only FIPS approved ciphers in the FIPS mode
Patch7:		gnutls-2.12.21-fips-algorithms.patch
Patch8:		gnutls-3.1.11-nosrp.patch

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

%package -n	%{libxssl}
Summary:	Library providing a secure layer (SSL)
Group:		System/Libraries
Requires:	%{libname} = %{version}

%description -n	%{libxssl}
This package contains a shared library for %{name}.

%package -n	%{devname}
Summary:	Development files for %{name}
Group:		Development/C
Requires:	%{name} = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}
Requires:	%{libnamexx} = %{version}-%{release}
Requires:	%{libssl} = %{version}-%{release}
Requires:	%{libxssl} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n	%{devname}
This package contains all necessary files to compile or develop
programs/libraries that use %{name}.

%package locales
Summary:	Locale files for GnuTLS
Group:		System/Internationalization 
BuildArch:	noarch
Conflicts:	%{mklibname gnutls 28} <= 3.1.9.1-1

%description
Locale files for GnuTLS main library.

%prep
%setup -qn %{name}-%{dirver}
%patch1 -p1 -b .rpath
# This patch is not applicable as we use nettle now but some parts will be
# later reused.
#%patch7 -p1 -b .fips
%patch8 -p1 -b .nosrp

sed 's/gnutls_srp.c//g' -i lib/Makefile.in
sed 's/gnutls_srp.lo//g' -i lib/Makefile.in


%build
%configure2_5x \
	--disable-static \
	--with-included-libtasn1=no \
	--disable-srp-authentication \
	--with-libz-prefix=%{_prefix} \
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
%doc NEWS README
%{_bindir}/[cgs]*
%{_bindir}/danetool
%{_bindir}/psktool
%{_bindir}/p11tool
%{_bindir}/ocsptool
%{_mandir}/man?/*
%{_infodir}/*

%files locales -f %{name}.lang

%files -n %{libname}
%{_libdir}/libgnutls.so.%{major}*

%files -n %{libnamexx}
%{_libdir}/libgnutlsxx.so.%{major}*

%files -n %{libssl}
%{_libdir}/libgnutls-openssl.so.%{sslmajor}*

%files -n %{libxssl}
%{_libdir}/libgnutls-xssl.so.%{xsslmajor}*

%files -n %{devname}
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/gnutls

