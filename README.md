# Pako32 CPU

## Overview

Pako32 is a simple 32-bit [RISC-V][RISC-V] CPU created as a learning project by
its authors. The project targets [the TinyFPGA BX board][TinyFPGA BX] which
comes with [the Lattice ICE40LP8K-CM81 FPGA chip][Lattice iCE40 LP/HX].

## Build and programming

Pako32 is built with [the Yosys Open SYnthesis Suite][YosysHQ] and uses [the
tinyprog tool][tinyprog] as its programmer. Refer to [Installation of the FPGA
toolchain](#installation-of-the-fpga-toolchain) for information how to obtain
the needed tools.

With the right toolchain available on `PATH`, the following steps synthesize the
CPU and program it onto a target TinyFPGA BX board:

```
$ make
$ make prog
```

## Installation of the FPGA toolchain

Steps for [openSUSE Tumbleweed][openSUSE Tumbleweed] (tested with 20230922):

```
$ sudo zypper install git gcc gcc-c++ make cmake bison flex \
    python3-devel python3-virtualenv eigen3-devel libffi-devel libftdi1-devel \
    libstdc++-devel libboost_filesystem-devel libboost_program_options-devel \
    libboost_iostreams-devel libboost_system-devel libboost_thread-devel \
    tcl-devel readline-devel

$ mkdir icestorm-build
$ cd icestorm-build

$ git clone https://github.com/YosysHQ/icestorm.git
$ cd icestorm
$ git checkout -b pako32 d20a5e9001f46262bf0cef220f1a6943946e421d
$ PREFIX=$HOME/opt/icestorm make -j$(nproc)
$ PREFIX=$HOME/opt/icestorm make install
$ cd ..

$ git clone https://github.com/YosysHQ/nextpnr.git
$ cd nextpnr
$ git checkout -b pako32 nextpnr-0.6
$ cmake . -DARCH=ice40 -DICESTORM_INSTALL_PREFIX=$HOME/opt/icestorm -DCMAKE_INSTALL_PREFIX=$HOME/opt/nextpnr
$ make -j$(nproc)
$ make install
$ cd ..

$ git clone https://github.com/YosysHQ/yosys.git
$ cd yosys
$ git checkout -b pako32 yosys-0.33
$ PREFIX=$HOME/opt/yosys make config-gcc
$ PREFIX=$HOME/opt/yosys make -j$(nproc)
$ PREFIX=$HOME/opt/yosys make install
$ cd ..

$ virtualenv ~/opt/tinyprog
$ source ~/opt/tinyprog/bin/activate
$ pip install tinyprog
$ deactivate

$ cd ~/bin
$ ln -s ../opt/icestorm/bin/icepack
$ ln -s ../opt/icestorm/bin/icetime
$ ln -s ../opt/nextpnr/bin/nextpnr-ice40
$ ln -s ../opt/yosys/bin/yosys
$ ln -s ../opt/tinyprog/bin/tinyprog
```

## License

This project is released under the terms of [the MIT License](COPYING).

[Lattice iCE40 LP/HX]: https://www.latticesemi.com/Products/FPGAandCPLD/iCE40
[RISC-V]: https://riscv.org/
[TinyFPGA BX]: https://www.crowdsupply.com/tinyfpga/tinyfpga-ax-bx
[YosysHQ]: https://github.com/YosysHQ
[openSUSE Tumbleweed]: https://get.opensuse.org/tumbleweed/
[tinyprog]: https://pypi.org/project/tinyprog/
