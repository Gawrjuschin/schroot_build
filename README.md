# shroot build project

This an example of how to build project using schroot environment with CMake.

## Usage
Required debian packages:

```bash
sudo apt install schroot debootstrap
```

Use file from `schroot/debian-trixie` as an example of config for schroot. 
Put it in `/etc/schroot/chroot.d` to make this chroot available. 
Don't forget to create directory scpecified in the `directory` in `schroot/debian-trixie`.

### Download chroot environment

Use debootstrap command to download and install chroot:

```bash
sudo debootstrap --arch amd64 trixie /srv/chroot/debian-trixie https://ftp.debian.org/debian/
```

### Switch chroot

To switch to schroot use command:

```bash
  sudo schroot -c debian-trixie -u user
```

### Compiler setup

Setup required compilers when on schroot. It is expected that in schroot environment the gcc, g++, (TODO: clang, clang++, lld) compilers are specified. Use following commands to enable alternatives (Debian 14 as an example):

```bash
sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-14 10
sudo update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-14 10
sudo update-alternatives --install /usr/bin/clang clang  /usr/bin/clang-21 10
sudo update-alternatives --install /usr/bin/clang++ clang++  /usr/bin/clang++-21 10
sudo update-alternatives --install /usr/bin/ld.lld ld.lld /usr/bin/ld.lld-21 10
```
