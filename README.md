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

Setup system gcc and g++ packages and it's multiarch versions for crosscompilation, `i686-linux-gnu-g++-14` for example. By default gcc installs with package <native>-linux-gnu-g++ package.


### Build 

Build project with package using command:

```bash
cmake --workflow --preset debian-trixie-x86_64-full
```

There is still single empty header file, but in future I'm going to add real library with tests.

### TODO
 - more arch support (at least for i686 and Arm64)
 - better presets separated by arch and OS
 - more complex examples
