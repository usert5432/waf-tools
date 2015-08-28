# Some tools for waf.



This repository holds some simple waf tools which help build code with waf.

## Preparing a custom copy of the waf command.

These tools are intended to be built into a custom copy of waf, likely
along with some provided in the `waflib/extras/` directory of the waf
source distribution.

Make some working area:

    $ mkdir -p /path/to/my/dev
    $ cd /path/to/my/dev

Get waf-tools:

    $ git clone git@github.com:BNLIF/waf-tools.git
	$ export MYWAFTOOLS=`pwd`/waf-tools  # <-- just to refer to later

Get and make waf:

    $ git clone https://github.com/waf-project/waf.git
    $ cd waf
	$ python waf-light --make-waf --prelude='' --tools=doxygen,boost,bjam,eigen3,rootsys,smplpkgs

Finally, copy the resulting `waf` into your top-level build area and
possibly commit it.  Because this tool is now "waf + extras" it is
recomended to give is a name other than `waf`.  Here, `mbt` is chosen,
short for "my build tool":

    $ cp waf /path/to/my/build/package/mbt


## Using the tools

In your top-level build area tools can be used in the "usual waf way".  In your `wscript` file simply `.load()` the tool by name.

# Using the `smplpkgs` tool to build suites of packages

The `smplpkgs` tool included in `waf-tools` provides a simple way to
build a suite of software packages that have interdependencies without
you, the developer, having to care much about the build system.

## Package organization 

To achieve this simplicity, some file and directory naminging
conventions and organization must be followed, as illustrated:

```
pkg1/
├── wscript_build
├── inc/
│   └── ProjectNamePkg1/*.h
├── src/*.{cxx,h}
└── test/*.{cxx,h}
pkg2/
├── wscript_build
├── inc/
│   └── ProjectNamePkg2/*.h
├── src/*.{cxx,h}
├── app/*.{cxx,h}
└── test/*.{cxx,h}
```

Specificx:

* All packages placed in a top-level directory (not required, but aggregating them via `git submodule` is useful).

* Public header files for the package must be placed under `<pkgdirname>/inc/<PackageName>/`,

* Library source (implementation and private headers) under `<pkgdirname>/src/`

* Application source (implementation and private headers) under `<pkgdirname>/app/` with only main application files and one application per `*.cxx` file.

* Test source (implementation and private headers) under `<pkgdirname>/test/` with main test programs named like `test_*.cxx`.

* A short `wscript_build` file in each package.

The `<pkgdirname>` only matters in the top-level `wscript` file which
you must provide.  The `<PackageName>` matters for inter-package
dependencies.

## The per-package `wscript_build` file

Each package needs a brief (generally single line) file called `wscript_build` to exist at in its top-level directory.  It is responsible for declaring:

- The package name
- Library dependencies
- Any additional application dependencies
- Any additional test dependencies

Example:

```python
bld.smplpkg('MyPackage', use='YourPackage YourOtherPackage')
```

Test and application programs are allowed to have additional dependencies declared.  For example:

```python
bld.smplpkg('MyPackage', use='YourPackage YourOtherPackage', test_use='ROOTSYS')
```

## The top-level `wscript` file

Driving the bild of all packages is a main `wscript` file.  It is responsible for:

- loading any tools in waf options/configure/build contexts
- recursing down into the package directories
- handling any special build instructions not supported by smplpkgs.

