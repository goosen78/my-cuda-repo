# Todo:
# - build cuda-gdb from source
# - /usr/include/cuda is owned by the cuda main package but the devel
#   subpackages use the directory
# - AppData for nsight-compute/systems

%global         debug_package %{nil}
%global         __strip /bin/true
%global         _missing_build_ids_terminate_build 0
%global         major_package_version 10-1

%if 0%{?rhel} == 6
%{?filter_setup:
%filter_from_provides /libQt5.*\.so.*/d; /libq.*\.so.*/d; /libicu.*\.so.*/d; /libssl\.so.*/d; /libcrypto\.so.*/d; /libstdc++\.so.*/d; /libprotobuf\.so.*/d; /libcupti\.so.*/d; /libboost_.*\.so.*/d
%filter_from_requires /libQt5.*\.so.*/d; /libq.*\.so.*/d; /libicu.*\.so.*/d; /libssl\.so.*/d; /libcrypto\.so.*/d; /libstdc++\.so.*/d; /libprotobuf\.so.*/d; /libcupti\.so.*/d; /libboost_.*\.so.*/d
%filter_setup
}
%else
%global         __provides_exclude ^(libQt5.*\\.so.*|libq.*\\.so.*|libicu.*\\.so.*|libssl\\.so.*|libcrypto\\.so.*|libstdc\\+\\+\\.so.*|libprotobuf\\.so.*|libcupti\\.so.*|libboost_.*\\.so.*)$
%global         __requires_exclude ^(libQt5.*\\.so.*|libq.*\\.so.*|libicu.*\\.so.*|libssl\\.so.*|libcrypto\\.so.*|libstdc\\+\\+\\.so.*|libprotobuf\\.so.*|libcupti\\.so.*|libboost_.*\\.so.*)$
%endif

Name:           cuda
Version:        10.1.243
Release:        1%{?dist}
Summary:        NVIDIA Compute Unified Device Architecture Toolkit
Epoch:          1
License:        NVIDIA License
URL:            https://developer.nvidia.com/cuda-zone
ExclusiveArch:  x86_64

Source0:        %{name}-%{version}-x86_64.tar.xz
Source1:        %{name}-gdb-%{version}.src.tar.gz
Source2:        %{name}-generate-tarball.sh
Source3:        %{name}.sh
Source4:        %{name}.csh
Source5:        nvcc.profile

Source10:       nsight.desktop
Source11:       nsight.appdata.xml
Source12:       nvvp.desktop
Source13:       nvvp.appdata.xml
Source14:       nv-nsight-cu.desktop
Source15:       nv-nsight-cu.wrapper
Source16:       nsight-sys.desktop
Source17:       nsight-sys.wrapper

Source19:       accinj64.pc
Source20:       cublas.pc
Source21:       cublasLt.pc
Source22:       cuda.pc
Source23:       cudart.pc
Source24:       cufft.pc
Source25:       cufftw.pc
Source26:       cuinj64.pc
Source27:       curand.pc
Source28:       cusolver.pc
Source29:       cusparse.pc
Source30:       nppc.pc
Source31:       nppial.pc
Source32:       nppicc.pc
Source33:       nppicom.pc
Source34:       nppidei.pc
Source35:       nppif.pc
Source36:       nppig.pc
Source37:       nppim.pc
Source38:       nppi.pc
Source39:       nppist.pc
Source40:       nppisu.pc
Source41:       nppitc.pc
Source42:       npps.pc
Source43:       nvgraph.pc
Source44:       nvml.pc
Source45:       nvrtc.pc
Source46:       nvToolsExt.pc
Source47:       nvjpeg.pc

BuildRequires:  ImageMagick
BuildRequires:  desktop-file-utils
# For RUNPATH removal
BuildRequires:  chrpath
# For execstack removal
BuildRequires:  execstack
BuildRequires:  perl(Getopt::Long)
%else
BuildRequires:  prelink
%endif

Requires:       %{name}-libs%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Conflicts:      %{name}-%{major_package_version} < %{?epoch:%{epoch}:}%{version}-%{release}
Conflicts:      %{name}-core-%{major_package_version} < %{?epoch:%{epoch}:}%{version}-%{release}
Conflicts:      %{name}-minimal-build-%{major_package_version} < %{?epoch:%{epoch}:}%{version}-%{release}
Conflicts:      %{name}-gpu-library-advisor-%{major_package_version} < %{?epoch:%{epoch}:}%{version}-%{release}
Conflicts:      %{name}-nvcc-%{major_package_version} < %{?epoch:%{epoch}:}%{version}-%{release}
Conflicts:      %{name}-nvprune-%{major_package_version} < %{?epoch:%{epoch}:}%{version}-%{release}

%description
CUDA is a parallel computing platform and programming model that enables
dramatic increases in computing performance by harnessing the power of the
graphics processing unit (GPU).

%package cli-tools
Summary:        Compute Unified Device Architecture command-line tools
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       %{name}-devel = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       expat >= 1.95
Conflicts:      %{name}-command-line-tools-%{major_package_version} < %{?epoch:%{epoch}:}%{version}-%{release}
Conflicts:      %{name}-gdb-%{major_package_version} < %{?epoch:%{epoch}:}%{version}-%{release}
Conflicts:      %{name}-memcheck-%{major_package_version} < %{?epoch:%{epoch}:}%{version}-%{release}
Conflicts:      %{name}-nvdisasm-%{major_package_version} < %{?epoch:%{epoch}:}%{version}-%{release}
Conflicts:      %{name}-nvprof-%{major_package_version} < %{?epoch:%{epoch}:}%{version}-%{release}

%description cli-tools
Contains the command line tools to debug and profile CUDA applications.

%package libs
Summary:        Compute Unified Device Architecture native run-time library
Requires(post): ldconfig
Conflicts:      %{name}-core-libs-%{major_package_version} < %{?epoch:%{epoch}:}%{version}
Conflicts:      %{name}-driver-dev-%{major_package_version} < %{?epoch:%{epoch}:}%{version}-%{release}
Conflicts:      %{name}-license-%{major_package_version} < %{?epoch:%{epoch}:}%{version}-%{release}
Conflicts:      %{name}-libraries-%{major_package_version} < %{?epoch:%{epoch}:}%{version}-%{release}
# Explicitly declare the dependency or libcuda.so.1()(64bit) will pull in xorg-x11-drv-cuda-libs
Requires:       nvidia-driver-cuda-libs%{_isa}

%description libs
Contains the CUDA run-time library required to run CUDA application natively.

%package extra-libs
Summary:        All runtime NVIDIA CUDA libraries
Requires(post): ldconfig
Requires:       %{name}-cublas = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       %{name}-cudart = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       %{name}-cufft = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       %{name}-cupti = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       %{name}-curand = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       %{name}-cusolver = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       %{name}-cusparse = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       %{name}-npp = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       %{name}-nvgraph = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       %{name}-nvjpeg = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       %{name}-nvrtc = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       %{name}-nvtx = %{?epoch:%{epoch}:}%{version}-%{release}
Conflicts:      %{name}-runtime-%{major_package_version} < %{?epoch:%{epoch}:}%{version}-%{release}

%description extra-libs
Metapackage that installs all runtime NVIDIA CUDA libraries.

%package cublas
Summary:        NVIDIA CUDA Basic Linear Algebra Subroutines (cuBLAS) libraries
Requires(post): ldconfig
Conflicts:      %{name}-cublas-%{major_package_version} < %{?epoch:%{epoch}:}%{version}-%{release}

%description cublas
The NVIDIA CUDA Basic Linear Algebra Subroutines (cuBLAS) library is a
GPU-accelerated version of the complete standard BLAS library that delivers 6x
to 17x faster performance than the latest MKL BLAS.

%package cublas-devel
Summary:        Development files for NVIDIA CUDA Basic Linear Algebra Subroutines (cuBLAS)
Requires:       %{name}-cublas%{_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Conflicts:      %{name}-cublas-dev-%{major_package_version} < %{?epoch:%{epoch}:}%{version}

%description cublas-devel
This package provides development files for the NVIDIA CUDA Basic Linear
Algebra Subroutines (cuBLAS) libraries.

%package cudart
Summary:        NVIDIA CUDA Runtime API library
Requires(post): ldconfig
Conflicts:      %{name}-cudart-%{major_package_version} < %{?epoch:%{epoch}:}%{version}-%{release}

%description cudart
The runtime API eases device code management by providing implicit initialization,
context management, and module management. This leads to simpler code, but it
also lacks the level of control that the driver API has.

In comparison, the driver API offers more fine-grained control, especially over
contexts and module loading. Kernel launches are much more complex to implement,
as the execution configuration and kernel parameters must be specified with
explicit function calls. However, unlike the runtime, where all the kernels are
automatically loaded during initialization and stay loaded for as long as the
program runs, with the driver API it is possible to only keep the modules that
are currently needed loaded, or even dynamically reload modules. The driver API
is also language-independent as it only deals with cubin objects.

%package cudart-devel
Summary:        Development files for NVIDIA CUDA Runtime API library
Requires:       %{name}-cudart%{_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Conflicts:      %{name}-cudart-dev-%{major_package_version} < %{?epoch:%{epoch}:}%{version}

%description cudart-devel
This package provides development files for the NVIDIA CUDA Runtime API library

%package cufft
Summary:        NVIDIA CUDA Fast Fourier Transform library (cuFFT) libraries
Requires(post): ldconfig
Conflicts:      %{name}-cufft-%{major_package_version} < %{?epoch:%{epoch}:}%{version}-%{release}

%description cufft
The NVIDIA CUDA Fast Fourier Transform libraries (cuFFT) provide a simple
interface for computing FFTs up to 10x faster.  By using hundreds of processor
cores inside NVIDIA GPUs, cuFFT delivers the floating‐point performance of a
GPU without having to develop your own custom GPU FFT implementation.

%package cufft-devel
Summary:        Development files for NVIDIA CUDA Fast Fourier Transform library (cuFFT)
Requires:       %{name}-cufft%{_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Conflicts:      %{name}-cufft-dev-%{major_package_version} < %{?epoch:%{epoch}:}%{version}

%description cufft-devel
This package provides development files for the NVIDIA CUDA Fast Fourier
Transform library (cuFFT) libraries.

%package cupti
Summary:        NVIDIA CUDA Profiling Tools Interface (CUPTI) library
Requires(post): ldconfig
Conflicts:      %{name}-cupti-%{major_package_version} < %{?epoch:%{epoch}:}%{version}-%{release}

%description cupti
The NVIDIA CUDA Profiling Tools Interface (CUPTI) provides performance analysis
tools with detailed information about how applications are using the GPUs in a
system.

%package cupti-devel
Summary:        Development files for NVIDIA CUDA Profiling Tools Interface (CUPTI) library
Requires:       %{name}-cupti%{_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Conflicts:      %{name}-cupti-dev-%{major_package_version} < %{?epoch:%{epoch}:}%{version}-%{release}

%description cupti-devel
This package provides development files for the NVIDIA CUDA Profiling Tools
Interface (CUPTI) library.

%package curand
Summary:        NVIDIA CUDA Random Number Generation library (cuRAND)
Requires(post): ldconfig
Conflicts:      %{name}-curand-%{major_package_version} < %{?epoch:%{epoch}:}%{version}-%{release}

%description curand
The NVIDIA CUDA Random Number Generation library (cuRAND) delivers high
performance GPU-accelerated random number generation (RNG). The cuRAND library
delivers high quality random numbers 8x faster using hundreds of processor
cores available in NVIDIA GPUs.

%package curand-devel
Summary:        Development files for NVIDIA CUDA Random Number Generation library (cuRAND)
Requires:       %{name}-curand%{_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Conflicts:      %{name}-curand-dev-%{major_package_version} < %{?epoch:%{epoch}:}%{version}

%description curand-devel
This package provides development files for the NVIDIA CUDA Random Number
Generation library (cuRAND).

%package cusolver
Summary:        NVIDIA cuSOLVER library
Requires(post): ldconfig
Requires:       libgomp%{_isa}
Conflicts:      %{name}-cusolver-%{major_package_version} < %{?epoch:%{epoch}:}%{version}-%{release}

%description cusolver
The NVIDIA cuSOLVER library provides a collection of dense and sparse direct
solvers which deliver significant acceleration for Computer Vision, CFD,
Computational Chemistry, and Linear Optimization applications.

%package cusolver-devel
Summary:        Development files for NVIDIA cuSOLVER library
Requires:       %{name}-cusolver%{_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Conflicts:      %{name}-cusolver-dev-%{major_package_version} < %{?epoch:%{epoch}:}%{version}

%description cusolver-devel
This package provides development files for the NVIDIA cuSOLVER library.

%package cusparse
Summary:        NVIDIA CUDA Sparse Matrix library (cuSPARSE) library
Requires(post): ldconfig
Conflicts:      %{name}-cusparse-%{major_package_version} < %{?epoch:%{epoch}:}%{version}-%{release}

%description cusparse
The NVIDIA CUDA Sparse Matrix library (cuSPARSE) provides a collection of basic
linear algebra subroutines used for sparse matrices that delivers up to 8x
faster performance than the latest MKL. The cuSPARSE library is designed to be
called from C or C++, and the latest release includes a sparse triangular
solver.

%package cusparse-devel
Summary:        Development files for NVIDIA CUDA Sparse Matrix library (cuSPARSE) library
Requires:       %{name}-cusparse%{_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Conflicts:      %{name}-cusparse-dev-%{major_package_version} < %{?epoch:%{epoch}:}%{version}

%description cusparse-devel
This package provides development files for the NVIDIA CUDA Sparse Matrix
library (cuSPARSE) library.

%package npp
Summary:        NVIDIA Performance Primitives libraries
Requires(post): ldconfig
Conflicts:      %{name}-npp-%{major_package_version} < %{?epoch:%{epoch}:}%{version}-%{release}

%description npp
The NVIDIA Performance Primitives library (NPP) is a collection of
GPU-accelerated image, video, and signal processing functions that deliver 5x
to 10x faster performance than comparable CPU-only implementations. Using NPP,
developers can take advantage of over 1900 image processing and approx 600
signal processing primitives to achieve significant improvements in application
performance in a matter of hours.

%package npp-devel
Summary:        Development files for NVIDIA Performance Primitives
Requires:       %{name}-npp%{_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Conflicts:      %{name}-npp-dev-%{major_package_version} < %{?epoch:%{epoch}:}%{version}

%description npp-devel
This package provides development files for the NVIDIA Performance Primitives
libraries.

%package nvgraph
Summary:        NVIDIA Graph Analytics library (nvGRAPH)
Requires(post): ldconfig
Conflicts:      %{name}-nvgraph-%{major_package_version} < %{?epoch:%{epoch}:}%{version}-%{release}

%description nvgraph
The NVIDIA Graph Analytics library (nvGRAPH) comprises of parallel algorithms
for high performance analytics on graphs with up to 2 billion edges. nvGRAPH
makes it possible to build interactive and high throughput graph analytics
applications.

%package nvgraph-devel
Summary:        Development files for NVIDIA Graph Analytics library (nvGRAPH)
Requires:       %{name}-nvgraph%{_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Conflicts:      %{name}-nvgraph-dev-%{major_package_version} < %{?epoch:%{epoch}:}%{version}

%description nvgraph-devel
This package provides development files for the NVIDIA Graph Analytics library
(nvGRAPH).

%package nvjpeg
Summary:        NVIDIA JPEG decoder (nvJPEG)
Requires(post): ldconfig
Conflicts:      %{name}-nvjpeg-%{major_package_version} < %{?epoch:%{epoch}:}%{version}-%{release}

%description nvjpeg
nvJPEG is a high-performance GPU-accelerated library for JPEG decoding. nvJPEG
supports decoding of single and batched images, color space conversion, multiple
phase decoding, and hybrid decoding using both CPU and GPU. Applications that
rely on nvJPEG for decoding deliver higher throughput and lower latency JPEG
decode compared CPU-only decoding.

%package nvjpeg-devel
Summary:        Development files for NVIDIA JPEG decoder (nvJPEG)
Requires:       %{name}-nvjpeg%{_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Conflicts:      %{name}-nvjpeg-dev-%{major_package_version} < %{?epoch:%{epoch}:}%{version}

%description nvjpeg-devel
This package provides development files for the NVIDIA JPEG decoder (nvJPEG).

%package nvml-devel
Summary:        Development files for NVIDIA Management library (nvML)
# Unversioned as it is provided by the driver's NVML library
Requires:       %{name}-nvml%{_isa}
Conflicts:      %{name}-nvml-dev-%{major_package_version} < %{?epoch:%{epoch}:}%{version}

%description nvml-devel
This package provides development files for the NVIDIA Management library
(nvML).

%package nvrtc
Summary:        NVRTC runtime compilation library
Requires(post): ldconfig
Conflicts:      %{name}-nvrtc-%{major_package_version} < %{?epoch:%{epoch}:}%{version}-%{release}

%description nvrtc
NVRTC is a runtime compilation library for CUDA C++. It accepts CUDA C++ source
code in character string form and creates handles that can be used to obtain
the PTX. The PTX string generated by NVRTC can be loaded by cuModuleLoadData and
cuModuleLoadDataEx, and linked with other modules by cuLinkAddData of the CUDA
Driver API. This facility can often provide optimizations and performance not
possible in a purely offline static compilation.

%package nvrtc-devel
Summary:        Development files for the NVRTC runtime compilation library
Requires:       %{name}-nvrtc%{_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Conflicts:      %{name}-nvrtc-dev-%{major_package_version} < %{?epoch:%{epoch}:}%{version}

%description nvrtc-devel
This package provides development files for the NVRTC runtime compilation
library.

%package nvtx
Summary:        NVIDIA Tools Extension
Requires(post): ldconfig
Conflicts:      %{name}-nvtx-%{major_package_version} < %{?epoch:%{epoch}:}%{version}-%{release}

%description nvtx
A C-based API for annotating events, code ranges, and resources in your
applications. Applications which integrate NVTX can use the Visual Profiler to
capture and visualize these events and ranges.

%package nvtx-devel
Summary:        Development files for NVIDIA Tools Extension
Requires:       %{name}-nvtx%{_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Conflicts:      %{name}-nvtx-dev-%{major_package_version} < %{?epoch:%{epoch}:}%{version}

%description nvtx-devel
This package provides development files for the NVIDIA Tools Extension.

%package devel
Summary:        Development files for %{name}
Requires:       %{name}%{_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       %{name}-libs%{_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       %{name}-cupti-devel%{_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       %{name}-cublas-devel%{_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       %{name}-cudart-devel%{_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       %{name}-cufft-devel%{_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       %{name}-cupti-devel%{_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       %{name}-curand-devel%{_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       %{name}-cusolver-devel%{_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       %{name}-cusparse-devel%{_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       %{name}-npp-devel%{_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       %{name}-nvgraph-devel%{_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       %{name}-nvjpeg-devel%{_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       %{name}-nvml-devel%{_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       %{name}-nvrtc-devel%{_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       %{name}-nvtx-devel%{_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Conflicts:      %{name}-headers-%{major_package_version} < %{?epoch:%{epoch}:}%{version}
Conflicts:      %{name}-libraries-dev-%{major_package_version} < %{?epoch:%{epoch}:}%{version}
Conflicts:      %{name}-misc-headers-%{major_package_version} < %{?epoch:%{epoch}:}%{version}
Conflicts:      %{name}-toolkit-%{major_package_version} < %{?epoch:%{epoch}:}%{version}
Obsoletes:      %{name}-static < %{?epoch:%{epoch}:}%{version}
Provides:       %{name}-static = %{?epoch:%{epoch}:}%{version}

%description devel
This package provides the development files of the %{name} package.

%package docs
Summary:        Compute Unified Device Architecture toolkit documentation
BuildArch:      noarch
Conflicts:      %{name}-documentation-%{major_package_version} < %{?epoch:%{epoch}:}%{version}

%description docs
Contains all guides and library documentation for CUDA.

%package samples
Summary:        Compute Unified Device Architecture toolkit samples
Conflicts:      %{name}-demo-suite-%{major_package_version} < %{?epoch:%{epoch}:}%{version}
Conflicts:      %{name}-samples-%{major_package_version} < %{?epoch:%{epoch}:}%{version}
Obsoletes:      %{name}-samples < %{?epoch:%{epoch}:}%{version}
Provides:       %{name}-samples = %{?epoch:%{epoch}:}%{version}
Requires:       cuda-devel = %{?epoch:%{epoch}:}%{version}
Requires:       cuda-gcc-c++
%else
Requires:       gcc-c++
%endif
Requires:       freeglut-devel
Requires:       make
Requires:       mesa-libGLU-devel
Requires:       libX11-devel
Requires:       libXmu-devel
Requires:       libXi-devel

%description samples
Contains an extensive set of example CUDA programs.

%package nsight
Summary:        NVIDIA Nsight Eclipse Edition
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Conflicts:      %{name}-nsight-%{major_package_version} < %{?epoch:%{epoch}:}%{version}-%{release}
Conflicts:      %{name}-visual-tools-%{major_package_version} < %{?epoch:%{epoch}:}%{version}-%{release}

%description nsight
NVIDIA Nsight Eclipse Edition is a full-featured IDE powered by the Eclipse
platform that provides an all-in-one integrated environment to edit, build,
debug and profile CUDA-C applications. Nsight Eclipse Edition supports a rich
set of commercial and free plugins.

%package nvvp
Summary:        NVIDIA Visual Profiler
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Conflicts:      %{name}-nvvp-%{major_package_version} < %{?epoch:%{epoch}:}%{version}-%{release}

%description nvvp
The NVIDIA Visual Profiler is a cross-platform performance profiling tool that
delivers developers vital feedback for optimizing CUDA C/C++ applications.

%package nsight-compute
Summary:        NVIDIA Nsight Compute
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Conflicts:      %{name}-nsight-compute-%{major_package_version} < %{?epoch:%{epoch}:}%{version}-%{release}

%description nsight-compute
NVIDIA Nsight Compute is an interactive kernel profiler for CUDA applications on
x86_64 platforms. It provides detailed performance metrics and API debugging via
a user interface and command line tool.

%package nsight-systems
Summary:        NVIDIA Nsight Systems
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Conflicts:      %{name}-nsight-systems-%{major_package_version} < %{?epoch:%{epoch}:}%{version}-%{release}

%description nsight-systems
NVIDIA Nsight Systems is a system-wide performance analysis tool designed to
visualize an application's algorithms, help you identify the largest
opportunities to optimize, and tune to scale efficiently across any quantity or
size of CPUs and GPUs; from large servers to the smallest SoC.

%prep
%setup -q -n %{name}-%{version}-x86_64

# Remove RUNPATH on binaries
chrpath -d cuda-toolkit/nvvm/bin/cicc
chrpath -d cuda-toolkit/NsightCompute-*/host/linux-desktop-glibc_*-x64/libicu*.so.*
chrpath -d cuda-toolkit/NsightSystems-*/Host-x86_64/libicu*.so.*
chrpath -d cuda-toolkit/NsightSystems-*/Host-x86_64/QdstrmImporter

# Replaced later
rm -f cuda-toolkit/bin/nvcc.profile

# RPMlint issues
find . -name "*.h" -exec chmod 644 {} \;
find . -name "*.hpp" -exec chmod 644 {} \;
find . -name "*.bat" -delete
find . -size 0 -delete

sed -i -e 's/env python/python2/g' cuda-samples/6_Advanced/matrixMulDynlinkJIT/extras/ptx2c.py

# Adjust path for NSight plugin
sed -i -e 's|`dirname $0`/..|/usr/lib64/nsight|g' cuda-toolkit/bin/nsight_ee_plugins_manage.sh

# Remove double quotes in samples' Makefiles (cosmetical)
find cuda-samples -name "Makefile" -exec sed -i -e 's|"/usr"|/usr|g' {} \;
# Make samples build without specifying anything on the command line for the
# include directories so people stop asking
find cuda-samples -type f -exec sed -i -e 's|/bin/nvcc|/bin/nvcc --include-path /usr/include/cuda|g' {} \;
find cuda-samples -name "Makefile" -exec sed -i -e 's|$(CUDA_PATH)/include|/usr/include/cuda|g' {} \;

%build
# Nothing to build

%install
# Create empty tree
mkdir -p %{buildroot}/usr/bin/
mkdir -p %{buildroot}/usr/share/applications/
mkdir -p %{buildroot}/usr/share/%{name}/
mkdir -p %{buildroot}/usr/share/libnsight/
mkdir -p %{buildroot}/usr/share/libnvvp/
mkdir -p %{buildroot}/usr/share/pixmaps/
mkdir -p %{buildroot}/usr/include/%{name}/
mkdir -p %{buildroot}/usr/lib64/pkgconfig/
mkdir -p %{buildroot}%{_libexecdir}/%{name}/
mkdir -p %{buildroot}/usr/share/man/man{1,3,7}/
mkdir -p %{buildroot}%{_sysconfdir}/profile.d/

# Environment settings
install -pm 644 %{SOURCE3} %{SOURCE4} %{buildroot}%{_sysconfdir}/profile.d

# Man pages
rm -f cuda-toolkit/doc/man/man1/cuda-install-samples-*
for man in cuda-toolkit/doc/man/man{1,3,7}/*; do gzip -9 $man; done
cp -fr cuda-toolkit/doc/man/* %{buildroot}/usr/share/man
# This man page conflicts with *a lot* of other packages
mv %{buildroot}/usr/share/man/man3/deprecated.3.gz \
    %{buildroot}/usr/share/man/man3/cuda_deprecated.3.gz
# Man page conflicts on properties
rm -f %{buildroot}/usr/share/man/man3/uuid.*

# Docs
mv cuda-toolkit/extras/Debugger/Readme.txt cuda-toolkit/extras/Debugger/Readme-Debugger.txt

# Headers
cp -fr cuda-toolkit/src %{buildroot}/usr/include/%{name}/fortran/
cp -fr cuda-toolkit/include/* cuda-toolkit/nvvm/include/* %{buildroot}/usr/include/%{name}/
cp -fr cuda-toolkit/extras/CUPTI/include %{buildroot}/usr/include/%{name}/CUPTI/
cp -fr cuda-toolkit/extras/Debugger/include %{buildroot}/usr/include/%{name}/Debugger/

# Libraries
cp -fr cuda-toolkit/%{_lib}/* cuda-toolkit/nvvm/%{_lib}/* %{buildroot}/usr/lib64/
cp -fr cuda-toolkit/extras/CUPTI/%{_lib}/* %{buildroot}/usr/lib64/
cp -fr cuda-toolkit/nvvm/libdevice/* %{buildroot}/usr/share/%{name}/

# Libraries in the driver package
ln -sf libnvidia-ml.so.1 %{buildroot}/usr/lib64/libnvidia-ml.so

# pkg-config files
install -pm 644 \
    %{SOURCE19} %{SOURCE20} %{SOURCE21} %{SOURCE22} %{SOURCE23} %{SOURCE24} \
    %{SOURCE25} %{SOURCE26} %{SOURCE27} %{SOURCE28} %{SOURCE29} %{SOURCE30} \
    %{SOURCE31} %{SOURCE32} %{SOURCE33} %{SOURCE34} %{SOURCE35} %{SOURCE36} \
    %{SOURCE37} %{SOURCE38} %{SOURCE39} %{SOURCE40} %{SOURCE41} %{SOURCE42} \
    %{SOURCE43} %{SOURCE44} %{SOURCE45} %{SOURCE46} %{SOURCE47} \
    %{buildroot}//usr/lib64/pkgconfig

# nvcc settings
install -pm 644 %{SOURCE5} %{buildroot}/usr/bin/

# Set proper variables
sed -i \
    -e 's|CUDA_VERSION|%{version}|g' \
    -e 's|LIBDIR|/usr/lib64|g' \
    -e 's|INCLUDE_DIR|/usr/include/cuda|g' \
    %{buildroot}//usr/lib64/pkgconfig/*.pc %{buildroot}//usr/bin/nvcc.profile

# Binaries
cp -fr cuda-toolkit/bin/* cuda-toolkit/nvvm/bin/* %{buildroot}/usr/bin/

# Additional samples
cp -fr cuda-samples %{buildroot}/usr/share/%{name}/samples
cp -fr cuda-toolkit/extras/CUPTI/samples %{buildroot}/usr/share/%{name}/samples/CUPTI
cp -fr cuda-toolkit/nvml/example %{buildroot}/usr/share/%{name}/samples/nvml
cp -fr cuda-toolkit/nvvm/libnvvm-samples %{buildroot}/usr/share/%{name}/samples/nvvm
cp -fr cuda-toolkit/extras/demo_suite %{buildroot}/usr/share/%{name}/

# Java stuff
sed -i -e '/^-vm/d' -e '/jre\/bin\/java/d' \
    cuda-toolkit/libnsight/nsight.ini cuda-toolkit/libnvvp/nvvp.ini
convert cuda-toolkit/libnsight/icon.xpm nsight.png
convert cuda-toolkit/libnvvp/icon.xpm nvvp.png
install -m 644 -p nsight.png %{buildroot}/usr/share/pixmaps/nsight.png
install -m 644 -p nvvp.png %{buildroot}/usr/share/pixmaps/nvvp.png
cp -fr cuda-toolkit/libnsight %{buildroot}/usr/lib64/nsight
cp -fr cuda-toolkit/libnvvp %{buildroot}/usr/lib64/nvvp
ln -sf /usr/lib64/nsight/nsight %{buildroot}/usr/bin/
ln -sf /usr/lib64/nvvp/nvvp %{buildroot}/usr/bin/
cp -fr cuda-toolkit/nsightee_plugins %{buildroot}/usr/lib64/nsight/

# QT programs
cp -fr cuda-toolkit/NsightCompute-* %{buildroot}/usr/lib64/NsightCompute
cp -fr cuda-toolkit/NsightSystems-* %{buildroot}/usr/lib64/NsightSystems
ln -sf /usr/lib64/NsightCompute/host/linux-desktop-glibc_2_11_3-x64/nv-nsight-cu.png \
    %{buildroot}/usr/share/pixmaps/nv-nsight-cu.png
ln -sf /usr/lib64/NsightSystems/host/Host-x86_64/nsight-sys.png \
    %{buildroot}/usr/share/pixmaps/nsight-sys.png
install -m 755 %{SOURCE15} %{buildroot}/usr/bin/nv-nsight-cu
install -m 755 %{SOURCE15} %{buildroot}/usr/bin/nsight-sys

# Desktop files
desktop-file-install --dir %{buildroot}/usr/share/applications/ \
    %{SOURCE10} %{SOURCE12} %{SOURCE14} %{SOURCE16}
desktop-file-validate %{buildroot}/usr/share/applications/nsight.desktop
desktop-file-validate %{buildroot}/usr/share/applications/nvvp.desktop
desktop-file-validate %{buildroot}/usr/share/applications/nv-nsight-cu.desktop
desktop-file-validate %{buildroot}/usr/share/applications/nsight-sys.desktop

%if 0%{?fedora}
# install AppData and add modalias provides
mkdir -p %{buildroot}/usr/share/appdata
install -p -m 0644 %{SOURCE11} %{SOURCE13} %{buildroot}/usr/share/appdata/
%endif

%ldconfig_scriptlets

%ldconfig_scriptlets cli-tools

%ldconfig_scriptlets libs

%ldconfig_scriptlets cublas

%ldconfig_scriptlets cudart

%ldconfig_scriptlets cufft

%ldconfig_scriptlets cupti

%ldconfig_scriptlets curand

%ldconfig_scriptlets cusolver

%ldconfig_scriptlets cusparse

%ldconfig_scriptlets npp

%ldconfig_scriptlets nvgraph

%ldconfig_scriptlets nvjpeg

%ldconfig_scriptlets nvrtc

%ldconfig_scriptlets nvtx

%files
/usr/bin/bin2c
/usr/bin/cicc
/usr/bin/crt/
/usr/bin/cudafe++
/usr/bin/cuobjdump
/usr/bin/gpu-library-advisor
/usr/bin/fatbinary
/usr/bin/nvcc
/usr/bin/nvcc.profile
/usr/bin/nvlink
/usr/bin/nvprune
/usr/bin/ptxas
%dir /usr/include/%{name}
/usr/libexec/%{name}/
/usr/share/man/man1/cuda-binaries.*
/usr/share/man/man1/cuobjdump.*
/usr/share/man/man1/nvcc.*
/usr/share/man/man1/nvprune.*
/usr/share/%{name}/
%exclude /usr/share/%{name}/samples
%exclude /usr/share/%{name}/demo_suite
%config(noreplace) %{_sysconfdir}/profile.d/%{name}.*sh

%files -n cli-tools
/usr/bin/cuda-gdb
/usr/bin/cuda-gdbserver
/usr/bin/cuda-memcheck
/usr/bin/nvdisasm
/usr/bin/nvprof
/usr/share/man/man1/cuda-gdb.*
/usr/share/man/man1/cuda-gdbserver.*
/usr/share/man/man1/cuda-memcheck.*
/usr/share/man/man1/nvdisasm.*
/usr/share/man/man1/nvprof.*

%files libs
%license cuda-toolkit/EULA.txt
/usr/lib64/libaccinj%{__isa_bits}.so.*
/usr/lib64/libcudart.so.*
/usr/lib64/libcuinj%{__isa_bits}.so.*
/usr/lib64/libnvvm.so.*

%files -n cublas
%license cuda-toolkit/EULA.txt
/usr/lib64/libcublas.so.*
/usr/lib64/libcublasLt.so.*
/usr/lib64/libnvblas.so.*

%files -n cublas-devel
/usr/include/%{name}/cublas*
/usr/include/%{name}/nvblas*
/usr/lib64/libcublas_static.a
/usr/lib64/libcublas.so
/usr/lib64/libcublasLt_static.a
/usr/lib64/libcublasLt.so
/usr/lib64/libnvblas.so
/usr/lib64/pkgconfig/cublas.pc
/usr/lib64/pkgconfig/cublasLt.pc

%files -n cudart
%license cuda-toolkit/EULA.txt
/usr/lib64/libcudart.so.*

%files -n cudart-devel
/usr/include/%{name}/crt
/usr/include/%{name}/cuda_device_runtime_api.h
/usr/include/%{name}/cuda_runtime.h
/usr/include/%{name}/cuda_runtime_api.h
/usr/include/%{name}/cudart_platform.h
/usr/lib64/libcudadevrt.a
/usr/lib64/libcudart_static.a
/usr/lib64/libcudart.so
/usr/lib64/libculibos.a
/usr/lib64/pkgconfig/cudart.pc

%files -n nvtx
%license cuda-toolkit/EULA.txt
/usr/lib64/libnvToolsExt.so.*

%files -n nvtx-devel
/usr/include/%{name}/nvToolsExt.h
/usr/include/%{name}/nvToolsExtCuda.h
/usr/include/%{name}/nvToolsExtCudaRt.h
/usr/include/%{name}/nvToolsExtMeta.h
/usr/include/%{name}/nvToolsExtSync.h
/usr/include/%{name}/nvtx3
/usr/lib64/libnvToolsExt.so
/usr/lib64/pkgconfig/nvToolsExt.pc

%files -n cufft
%license cuda-toolkit/EULA.txt
/usr/lib64/libcufft.so.*
/usr/lib64/libcufftw.so.*

%files -n cufft-devel
/usr/include/%{name}/cufft*
/usr/lib64/libcufft_static.a
/usr/lib64/libcufft_static_nocallback.a
/usr/lib64/libcufft.so
/usr/lib64/libcufftw_static.a
/usr/lib64/libcufftw.so
/usr/lib64/pkgconfig/cufft.pc
/usr/lib64/pkgconfig/cufftw.pc

%files -n cupti
%license cuda-toolkit/EULA.txt
/usr/lib64/libcupti.so.*

%files -n cupti-devel
%doc cuda-toolkit/extras/CUPTI/doc/*
/usr/include/%{name}/CUPTI
/usr/lib64/libcupti_static.a
/usr/lib64/libcupti.so
/usr/lib64/libnvperf_host.so
/usr/lib64/libnvperf_host_static.a
/usr/lib64/libnvperf_target.so

%files -n curand
%license cuda-toolkit/EULA.txt
/usr/lib64/libcurand.so.*

%files -n curand-devel
/usr/include/%{name}/curand*
/usr/include/%{name}/sobol_direction_vectors.h
/usr/lib64/libcurand_static.a
/usr/lib64/libcurand.so
/usr/lib64/pkgconfig/curand.pc

%files -n cusolver
%license cuda-toolkit/EULA.txt
/usr/lib64/libcusolver.so.*

%files -n cusolver-devel
/usr/include/%{name}/cusolver*
/usr/lib64/libcusolver_static.a
/usr/lib64/libcusolver.so
/usr/lib64/liblapack_static.a
/usr/lib64/libmetis_static.a
/usr/lib64/pkgconfig/cusolver.pc

%files -n cusparse
%license cuda-toolkit/EULA.txt
/usr/lib64/libcusparse.so.*

%files -n cusparse-devel
/usr/include/%{name}/cusparse*
/usr/lib64/libcusparse_static.a
/usr/lib64/libcusparse.so
/usr/lib64/pkgconfig/cusparse.pc

%files -n npp
%license cuda-toolkit/EULA.txt
/usr/lib64/libnpp*.so.*

%files -n npp-devel
/usr/include/%{name}/npp*
/usr/lib64/libnpp*_static.a
/usr/lib64/libnpp*.so
/usr/lib64/pkgconfig/npp*.pc

%files -n nvgraph
%license cuda-toolkit/EULA.txt
/usr/lib64/libnvgraph_static.a
/usr/lib64/libnvgraph.so.*

%files -n nvgraph-devel
/usr/include/%{name}/nvgraph*
/usr/lib64/libnvgraph.so
/usr/lib64/pkgconfig/nvgraph.pc

%files -n nvjpeg
%license cuda-toolkit/EULA.txt
/usr/lib64/libnvjpeg_static.a
/usr/lib64/libnvjpeg.so.*

%files -n nvjpeg-devel
/usr/include/%{name}/nvjpeg.h
/usr/lib64/libnvjpeg.so
/usr/lib64/pkgconfig/nvjpeg.pc

%files -n nvml-devel
/usr/include/%{name}/nvml*
/usr/lib64/libnvidia-ml.so
/usr/lib64/pkgconfig/nvml.pc

%files -n nvrtc
%license cuda-toolkit/EULA.txt
/usr/lib64/libnvrtc-builtins.so.*
/usr/lib64/libnvrtc.so.*

%files -n nvrtc-devel
/usr/include/%{name}/nvrtc*
/usr/lib64/libnvrtc-builtins.so
/usr/lib64/libnvrtc.so
/usr/lib64/pkgconfig/nvrtc.pc

%files  dev
%doc cuda-toolkit/extras/Debugger/Readme-Debugger.txt
/usr/include/%{name}/CL
/usr/include/%{name}/Debugger
/usr/include/%{name}/builtin_types.h
/usr/include/%{name}/channel_descriptor.h
/usr/include/%{name}/common_functions.h
/usr/include/%{name}/cooperative_groups.h
/usr/include/%{name}/cooperative_groups_helpers.h
/usr/include/%{name}/cuComplex.h
/usr/include/%{name}/cuda.h
/usr/include/%{name}/cudaEGL.h
/usr/include/%{name}/cudaGL.h
/usr/include/%{name}/cudaProfiler.h
/usr/include/%{name}/cudaVDPAU.h
/usr/include/%{name}/cuda_egl_interop.h
/usr/include/%{name}/cuda_fp16.h
/usr/include/%{name}/cuda_fp16.hpp
/usr/include/%{name}/cuda_gl_interop.h
/usr/include/%{name}/cuda_occupancy.h
/usr/include/%{name}/cuda_profiler_api.h
/usr/include/%{name}/cuda_surface_types.h
/usr/include/%{name}/cuda_texture_types.h
/usr/include/%{name}/cuda_vdpau_interop.h
/usr/include/%{name}/cudalibxt.h
/usr/include/%{name}/device_atomic_functions.h
/usr/include/%{name}/device_atomic_functions.hpp
/usr/include/%{name}/device_double_functions.h
/usr/include/%{name}/device_functions.h
/usr/include/%{name}/device_launch_parameters.h
/usr/include/%{name}/device_types.h
/usr/include/%{name}/driver_functions.h
/usr/include/%{name}/driver_types.h
/usr/include/%{name}/fatBinaryCtl.h
/usr/include/%{name}/fatbinary.h
/usr/include/%{name}/fatbinary_section.h
/usr/include/%{name}/fortran  
/usr/include/%{name}/host_config.h
/usr/include/%{name}/host_defines.h
/usr/include/%{name}/library_types.h
/usr/include/%{name}/math_constants.h
/usr/include/%{name}/math_functions.h
/usr/include/%{name}/mma.h
/usr/include/%{name}/nvfunctional
/usr/include/%{name}/nvvm.h
/usr/include/%{name}/sm_20_atomic_functions.h
/usr/include/%{name}/sm_20_atomic_functions.hpp
/usr/include/%{name}/sm_20_intrinsics.h
/usr/include/%{name}/sm_20_intrinsics.hpp
/usr/include/%{name}/sm_30_intrinsics.h
/usr/include/%{name}/sm_30_intrinsics.hpp
/usr/include/%{name}/sm_32_atomic_functions.h
/usr/include/%{name}/sm_32_atomic_functions.hpp
/usr/include/%{name}/sm_32_intrinsics.h
/usr/include/%{name}/sm_32_intrinsics.hpp
/usr/include/%{name}/sm_35_atomic_functions.h
/usr/include/%{name}/sm_35_intrinsics.h
/usr/include/%{name}/sm_60_atomic_functions.h
/usr/include/%{name}/sm_60_atomic_functions.hpp
/usr/include/%{name}/sm_61_intrinsics.h
/usr/include/%{name}/sm_61_intrinsics.hpp
/usr/include/%{name}/surface_functions.h
/usr/include/%{name}/surface_functions.hpp
/usr/include/%{name}/surface_indirect_functions.h
/usr/include/%{name}/surface_indirect_functions.hpp
/usr/include/%{name}/surface_types.h
/usr/include/%{name}/texture_fetch_functions.h
/usr/include/%{name}/texture_fetch_functions.hpp
/usr/include/%{name}/texture_indirect_functions.h
/usr/include/%{name}/texture_indirect_functions.hpp
/usr/include/%{name}/texture_types.h
/usr/include/%{name}/thrust
/usr/include/%{name}/vector_functions.h
/usr/include/%{name}/vector_functions.hpp
/usr/include/%{name}/vector_types.h
/usr/lib64/libaccinj%{__isa_bits}.so
/usr/lib64/libcuinj%{__isa_bits}.so
/usr/lib64/libnvvm.so
/usr/share/man/man3/*
/usr/share/man/man7/*
/usr/lib64/pkgconfig/accinj64.pc
/usr/lib64/pkgconfig/cuda.pc
/usr/lib64/pkgconfig/cuinj64.pc

%files docs
%doc cuda-toolkit/doc/pdf cuda-toolkit/doc/html cuda-toolkit/tools/*

%files -n samples
/usr/share/%{name}/samples
/usr/share/%{name}/demo_suite

%files -n nsight
/usr/bin/nsight
/usr/bin/nsight_ee_plugins_manage.sh
/usr/share/appdata/nsight.appdata.xml
/usr/share/applications/nsight.desktop
/usr/share/pixmaps/nsight.png
/usr/lib64/nsight
/usr/share/man/man1/nsight.*

%files -n nvvp
/usr/bin/computeprof
/usr/bin/nvvp
/usr/share/appdata/nvvp.appdata.xml
/usr/share/applications/nvvp.desktop
/usr/share/pixmaps/nvvp.png
/usr/share/man/man1/nvvp.*
/usr/lib64/nvvp

%files -n nsight-compute
/usr/bin/nv-nsight-cu
/usr/share/applications/nv-nsight-cu.desktop
/usr/share/pixmaps/nv-nsight-cu.png
/usr/lib64/NsightCompute

%files -n nsight-systems
/usr/bin/nsight-sys
/usr/share/applications/nsight-sys.desktop
/usr/share/pixmaps/nsight-sys.png
/usr/lib64/NsightSystems
