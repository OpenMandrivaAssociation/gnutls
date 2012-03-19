%define	libgcrypt_version 1.2.4

%define	major	28
%define	sslmajor 27
%define	libname	%mklibname %{name} %{major}
%define	libssl	%mklibname %{name}-ssl %{sslmajor}
%define	devname	%mklibname %{name} -d

Summary:	Library providing a secure layer (SSL)
Name:		gnutls
Version:	3.0.17
Release:	1
License:	GPLv2+ and LGPLv2+
Group:		System/Libraries
URL:		http://www.gnutls.org
Source0:	http://ftp.gnu.org/pub/gnu/gnutls/%{name}-%{version}.tar.xz
Source1:	http://ftp.gnu.org/pub/gnu/gnutls/%{name}-%{version}.tar.xz.sig
Patch0:		gnutls-2.12.7-dsa-skiptests.patch
Patch1:		gnutls-2.12.11-rpath.patch
BuildRequires:	liblzo-devel
BuildRequires:	libgcrypt-devel >= %{libgcrypt_version}
BuildRequires:	libtasn1-devel >= 0.3.4
BuildRequires:	p11-kit-devel
BuildRequires:	pkgconfig(nettle)
%ifnarch %{arm} %{mips}
BuildRequires:	valgrind
%endif

%description
GnuTLS is a project that aims to develop a library which provides 
a secure layer, over a reliable transport layer.

%package -n	%{libname}
Summary:	Library providing a secure layer (SSL)
Group:		System/Libraries

%description -n	%{libname}
GnuTLS is a project that aims to develop a library which provides
a secure layer, over a reliable transport layer.

%package -n	%{libssl}
Summary:        Library providing a secure layer (SSL)
Group:          System/Libraries

%description -n	%{libssl}
GnuTLS is a project that aims to develop a library which provides
a secure layer, over a reliable transport layer.

%package -n	%{devname}
Summary:	Development files for %{name}
Group:		Development/C
Requires:	%{name} = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}
Requires:	%{libssl} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Requires:	libgcrypt-devel >= %{libgcrypt_version}
Obsoletes:	%mklibname %{name} 13 -d

%description -n	%{devname}
GnuTLS is a project that aims to develop a library which provides
a secure layer, over a reliable transport layer.

This package contains all necessary files to compile or develop
programs/libraries that use %{name}.

%prep
%setup -q
#patch0 -p1
#patch1 -p1 -b .rpath~

%build
%configure2_5x \
	--with-included-libtasn1=no \
	--with-included-libcfg=yes \
	--with-lzo \
	--with-libz-prefix=%{_prefix} \
	--with-libgcrypt \
	--with-libgcrypt-prefix=%{_prefix} \
	--with-libtasn1-prefix=%{_prefix} \
%ifnarch %{arm} %{mips}
	--enable-valgrind-tests \
%endif
	--disable-rpath \
	--disable-guile

%make

%check
make check

%install
%makeinstall_std
%find_lang gnutls

%post
%_install_info gnutls.info

%postun
%_remove_install_info gnutls.info

%files
%doc NEWS README
%_bindir/[cgs]*
%_bindir/psktool
%_bindir/p11tool
%_bindir/ocsptool
%_mandir/man?/*
%_infodir/*

%files -n %{libname} -f gnutls.lang
%{_libdir}/lib*.so.%{major}*

%files -n %{libssl}
%{_libdir}/lib*.so.%{sslmajor}*

%files -n %{devname}
%{_libdir}/*.so
%{_libdir}/*.a
%{_libdir}/pkgconfig/*.pc
%{_includedir}/gnutls
