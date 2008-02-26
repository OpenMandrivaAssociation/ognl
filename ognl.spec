# Copyright (c) 2000-2007, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

%define gcj_support 1

Summary:        Object-Graph Navigation Language
Name:           ognl
Version:        2.6.9
Release:        %mkrel 2.0.1
Epoch:          0
License:        BSD -style
URL:            http://www.ognl.org/
Group:          Development/Java
Source0:        http://www.ognl.org/%{version}/%{name}-%{version}-dist.zip
Source1:        http://www.ognl.org/%{version}/%{name}-%{version}-doc.zip
Source2:        ognl-osbuild.xml
Source3:        ognl-copyright.html
BuildRequires:  jpackage-utils >= 0:1.6
BuildRequires:  java-rpmbuild
BuildRequires:  ant >= 0:1.6
BuildRequires:  ant-junit >= 0:1.6
BuildRequires:  ant-nodeps >= 0:1.6
BuildRequires:  ant-trax
BuildRequires:  ant-contrib
BuildRequires:  junit
BuildRequires:  javacc
BuildRequires:  javassist
%if %{gcj_support}
BuildRequires:          java-gcj-compat-devel
%endif
%if ! %{gcj_support}
BuildArch:      noarch
%endif
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
OGNL stands for Object-Graph Navigation Language; it is an 
expression language for getting and setting properties of 
Java objects. You use the same expression for both getting 
and setting the value of a property. 
The ognl.Ognl class contains convenience methods for evaluating 
OGNL expressions. You can do this in two stages, parsing an 
expression into an internal form and then using that internal 
form to either set or get the value of a property; or you can 
do it in a single stage, and get or set a property using the 
String form of the expression directly. 
Many people have asked exactly what OGNL is good for. Several 
of the uses to which OGNL has been applied are: 
* A binding language between GUI elements (textfield, combobox, 
  etc.) to model objects. Transformations are made easier by 
  OGNL's TypeConverter mechanism to convert values from one 
  type to another (String to numeric types, for example). 
* A data source language to map between table columns and a 
  TableModel. 
* A binding language between web components and the underlying 
  model objects (WebOGNL, Tapestry and WebWork). 
* A more expressive replacement for the property-getting 
  language used by the Jakarta Commons BeanUtils package 
  (which only allows simple property navigation and 
  rudimentary indexed properties). 
Most of what you can do in Java is possible in OGNL, plus other 
extras such as list projection and selection and lambda expressions.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java

%description javadoc
%{summary}.

%package manual
Summary:        Manual for %{name}
Group:          Development/Java

%description manual
%{summary}.

%prep
%setup -q -c -n %{name}-%{version}
unzip -qq %{SOURCE1}
# remove all binary libs
%remove_java_binaries
cp %{SOURCE2} osbuild.xml

%build
build-jar-repository -s -p lib  \
ant-contrib \
javacc \
junit \
javassist \

export OPT_JAR_LIST="ant-contrib ant-launcher ant/ant-nodeps ant/ant-junit ant/ant-trax junit javacc"
%ant jar javadocs junit.report

%install
rm -rf $RPM_BUILD_ROOT

# jars
install -d -m 0755 $RPM_BUILD_ROOT%{_javadir}

install -m 0644 build/%{name}-%{version}.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}.jar; do ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`; done)

# javadoc
install -d -m 0755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr dist/docs/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name}

# manual
install -d -m 0755 $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/html
install -d -m 0755 $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/pdf
cp -pr docs/html/* $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/html
cp -pr docs/pdf/* $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/pdf
cp -pr docs/index.html $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
cp -p %{SOURCE3} $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/copyright.html

%{gcj_compile}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(0644,root,root,0755)
%doc %{_docdir}/%{name}-%{version}/copyright.html
%{_javadir}/*.jar
%{gcj_files}

%files javadoc
%defattr(0644,root,root,0755)
%{_javadocdir}/%{name}-%{version}
%{_javadocdir}/%{name}

%files manual
%defattr(0644,root,root,0755)
%doc %{_docdir}/%{name}-%{version}/index.html
%doc %{_docdir}/%{name}-%{version}/html
%doc %{_docdir}/%{name}-%{version}/pdf
