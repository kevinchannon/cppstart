# CPP Start
`cppstart` is a simple command-line tool to initialise a reasonable C++ project.

## Get `cppstart`
`cppstart` is a python application, so you'll need a working Python install to use it. Once you have Python, then you can simply do `pip install cppstart` to install cppstart

## Creating a C++ project
Say you want to create a new C++ application called "foo" in the current directory. Then just do:
```shell
cppstart foo
```
That's it!

### What do you get?
Once you've run cppstart, you should see a new directory in the current folder with the name you specified for your project. In there, you will find:
* Some `init` scripts. There are `.sh` and `.ps1` versions, for initialising your project on Linux and Windows, respectively. (Technically, the scripts run in Bash and Powershell, so you can use the `.sh` version on Windows too, if you run it in something like GitBash). The initialisation process basically just pulls all the third-party dependencies that your  project requires. When first iniitalised, it only has one dependency: Catch2, for writing unit tests.
* Some `build` scripts. There are `.sh` and `.ps1` versions, for builing your project on Linux and Windows, respectively. (Technically, the scripts run in Bash and Powershell, so you can use the `.sh` version on Windows too, if you run it in something like GitBash). The build scripts run CMake to build your source code into an app/library.
* 