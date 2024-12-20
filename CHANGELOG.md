# rocPyDecode changelog

Full documentation for for rocPyDecode is available at [https://rocm.docs.amd.com/projects/rocPyDecode/en/latest/](https://rocm.docs.amd.com/projects/rocPyDecode/en/latest/)

## (Unreleased) rocPyDecode 0.3.0

### Added

### Changed

* AMD Clang is now the default CXX and C compiler.

### Removed

### Optimized

### Resolved issues


## rocPyDecode 0.2.0 for ROCm 6.3

### Added

* RGB and YUV pytorch tensors
* Python distribution wheel (.whl)
* Multiple usecase samples

### Changed

* Clang is now the default CXX compiler.

### Removed

* Make tests have been removed. CTEST is now used for both Make tests and package tests.
* hipcc. Clang is now the default CXX compiler.

### Optimized

* Setup Script: Build and runtime install options
* Pre-requisite installation helper python scripts
* Same GPU memory viewed as pytorch tensor

### Resolved issues

* Setup
  * no dependency on hipcc
  * building rocPyDecode only once

## rocPyDecode 0.1.0

### Additions

* Clang - Default CXX compiler
* Full rocDecode functionality
* Supporting all rocDecode codecs

### Optimizations

* Setup Script - Build and runtime install options
* pre-requisite installation helper python scripts

### Changes

* Samples - added more use cases samples
* Supported codecs - a check is added

### Fixes

### Upcoming changes
* Clang - Default CXX compiler
* Supported codecs - adding check if the input video codec is supported
* Setup to produce python wheel for end-user

