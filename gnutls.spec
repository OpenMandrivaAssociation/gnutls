# older opencdk forgot to bundle m4 file
%define opencdk_version 0.6.0
%define libgcrypt_version 1.2.4

%define major 26
%define libname %mklibname %{name} %{major}
%define libname_orig lib%{name}
%define develname %mklibname %{name} -d

Summary:	Library providing a secure layer (SSL)
Name:		gnutls
Version:	2.8.4
Release:	%mkrel 1
License:	GPLv2+ and LGPLv2+
Group:		System/Libraries
URL:		http://www.gnutls.org
Source0:	http://ftp.gnu.org/pub/gnu/gnutls/%{name}-%{version}.tar.bz2
Source1:	%{SOURCE0}.sig
# adapted from upstream commit c7e003ad9427c655a1b559baff1239a2c1907f32
#Patch0:		gnutls-2.8.1-allow_interrupted.patch
BuildRequires:	opencdk-devel >= %{opencdk_version}
BuildRequires:	liblzo-devel
BuildRequires:	libgcrypt-devel >= %{libgcrypt_version}
BuildRequires:	libtasn1-devel >= 0.3.4
BuildRequires:	valgrind
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

%description
GnuTLS is a project that aims to develop a library which provides 
a secure layer, over a reliable transport layer.

%package -n %{libname}
Summary:	Library providing a secure layer (SSL)
Group:		System/Libraries
Provides:	%{libname_orig} = %{version}-%{release}

%description -n	%{libname}
GnuTLS is a project that aims to develop a library which provides
a secure layer, over a reliable transport layer.

%package -n %{develname}
Summary:	Development files for %{name}
Group:		Development/C
Requires:	%{name} = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}
Provides:	%{libname_orig}-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Requires:	opencdk-devel >= %{opencdk_version}
Requires:	libgcrypt-devel >= %{libgcrypt_version}
Obsoletes:	%mklibname %{name} 13 -d

%description -n	%{develname}
GnuTLS is a project that aims to develop a library which provides
a secure layer, over a reliable transport layer.

This package contains all necessary files to compile or develop
programs/libraries that use %{name}.

%prep
%setup -q
#%patch0 -p1

%build
%configure2_5x \
	--with-included-libtasn1=no \
	--with-included-libcfg=yes \
	--with-lzo \
	--with-libz-prefix=%{_prefix} \
	--with-libgcrypt \
	--with-libgcrypt-prefix=%{_prefix} \
	--with-libtasn1-prefix=%{_prefix} \
	--disable-rpath \
	--disable-guile \
	--enable-valgrind-tests

%make

%check
make check

%install
rm -rf %{buildroot}
%makeinstall_std

%{find_lang} %{name} %{name} libgnutls

%clean
rm -rf %{buildroot}

%post
%_install_info gnutls.info

%if %mdkversion < 200900
%post -p /sbin/ldconfig -n %{libname}
%endif

%postun
%_remove_install_info gnutls.info

%if %mdkversion < 200900
%postun -p /sbin/ldconfig -n %{libname}
%endif

%files -f %{name}.lang 
%defattr(-,root,root)
%doc ChangeLog NEWS README
%{_bindir}/[cgs]*
%{_bindir}/psktool
%{_mandir}/man?/*
%{_infodir}/gnutls*

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/lib*.so.%{major}*

%files -n %{develname}
%defattr(-,root,root)
%{_libdir}/*.so
%{_libdir}/*.a
%{_libdir}/*.la
%{_libdir}/pkgconfig/*.pc
%{_includedir}/gnutls
