# CPP Start
`cppstart` is a simple command-line tool to initialise a reasonable C++ project.
## Motivation
When you first start writing C++, you will likely be confronted with an instruction like this:
1. Make a file that looks like this and save it to main.cpp:
    ```c++
   #include <iostream>
   
   int main() {
      std::cout << "Hello, World!" << std::endl;

      return 0;
   }
   ```
2. On a command line, do `g++ main.cpp -o a.out`
3. Congratulations! You're now a C++ programmer!

This is disastrously simple advice for nascent C++ developers. Creating a fully-fledged C++ project is _hard_. Making out that it's not hard is lulling people into a false sense of security. Imagine I google for "how to keep a lion as a pet" and I find:
1. Buy a lion cub
2. Congratulations! You are now have a pet lion. Have fun!

This is not sensible advice for lion ownership. You're going to need a few more pieces of PPE and various other equipment if you want to avoid disembowelment at some point in your fairly near future.

Typically, then, a project will start with a person hacking away at a main() in a project and running it to check the results. Quickly, some kind of build system, like CMake, will be needed. Then, at some point, they will decide that they should be using some kind of source control. Then, a bit later, maybe some kind of unit tests would be good and this code should probably be split into separate files, and maybe a library. But, **le sigh** getting some kind of unit test library in place requires managing the dependency on it. Who has time for all that!? It's easy enough to just copy the code into our repo and fix up the CMake files to use it properly

And this is how things progress, slowly either transforming into a sensible project, or just... not.

### A kick-start!
CppStart allows a user to quickly start a new application or library project with a fairly complete "devops" infrastructure in place. This means that, right from the start, you will have in place unit tests, code formatting, source control, continuous integration build & test, release pipelines and more.

**NOTE:** What cppstart DOESN'T DO is apply any updates to the project once it's made, or add all the goodness to an existing project, or anything like that. It's a fire-once-and-then-you're-on-your-own kind of a thing.

## Get `cppstart`
`cppstart` is a python application, so you'll need a working Python install to use it. Once you have Python, then you can simply do `pip install cppstart` to install cppstart

### (Meta) dependencies
The project that you create with cppstart will have a bunch of things that it needs for smooth running. These include:
* Git
* Some kind of C++ compiler (MSVC++, GCC, Clang, whatever)
* CMake
* Conan
* Clang-Format

To initialise the project, then you'll need a connection to the internet too, since it will need to pull down Catch2 to use for unit testing your code.

## Creating a C++ project
Say you want to create a new C++ application called "foo" in the current directory. Then just do:
```shell
cppstart foo
```
That's it!

If you want to create a library, called `bar`, then you simply do:
```commandline
cppstart --lib bar
```
And you're off.

### What do you get?
Once you've run `cppstart`, you should see a new directory in the current folder with the name you specified for your project. In there, you will find a bunch of files and directories:
```
/foo/
|-- .clang-format           <--- Formats your code for you, if yo have Clang installed
|-- /.git                   <--- Source control. You probably know what Git is! The repo
|                                is initialised and all the files are committed, ready to
|                                push somewhere.
|-- /.github
|   `-- /workflows          <--- Things in here provide CI if you push your code to Github
|      |-- build_and_test_ubuntu_gcc12_x64_debug.yml
|      |-- build_and_test_ubuntu_gcc12_x64_release.yml
|      |-- build_and_test_windows_msvc_x64_debug.yml
|      |-- build_and_test_windows_msvc_x64_release.yml
|      `-- release.yml
|-- .gitignore              <--- Pre-populated with a bunch of common files that you don't
|                                want to commit
|-- CMakeLists.txt          <--- Top-level build system file for the projec
|-- CODE_OF_CONDUCT.md
|-- CONTRIBUTING.md
|-- LICENSE                 <--- Text for the license that you specified when creating the
|                                project. Will default to the MIT license,
|-- README.md               <--- Initialised with some common section headings to prompt you
|-- SECURITY.md
|-- build.ps1               <--\    These build files can be called from the command line to
|-- build.sh*                   |-- build your code. There are shell and Powerhell versions
|                           <--/    that do the same thing, for running on Windows or Linux
|-- conanfile.txt           <--- This pulls in third-party dependencies via Conan. It's used
|                                by the "init" scripts. You can add new dependencies to it, as
|                                your project develops and you need more third-party libs 
|-- /examples               <--- Help your users with some working examples of how your code
|                                works. If you created an APP project, then this directory
|                                won't be here. You will run your project via src/main.cpp
|                                instead.
|   |-- CMakeLists.txt
|  `-- main.cpp
|-- /include                <--- The header files go in here.
|   `-- /foo
|       `-- foo.hpp
|-- init.ps1                <--\    These files are called when you first create the project, to
|-- init.sh*                    |-- pull in the dependencies that the project requires to build.
|                           <--/    There are shell and Powershell versions, for Linux and Windows
|-- /src                    <--- Your project sources go in here
|   |-- CMakeLists.txt
|   |-- /foo
|   |   `-- foo.cpp 
|   `-- main.cpp            <--- This is the "main" file for your app. If you created a LIB
|                                project, then this file won't be here. You'll run your library
|                                code via the examples and the tests in that case.
`-- /test                   <--- The unit tests for your project go in here. There is an initial
    |                            (failing) test to get you going :)
    |-- CMakeLists.txt
    `-- foo.test.cpp
```

## Initialise and build your project
The complete instructions to create, build and test an application called, say, "magic" look like this:
```shell
cppstart magic                          # Create the project
cd magic                                # Go into the project's directory
./init.sh                               # Get the necessary 3rd party libs (i.e. Catch2 for testing)
./build.sh                              # Build the project
./out/build/x64/test/Debug/magicTest    # Run the tests
```
When you run the tests, you should see some output that looks like this:
```shell
$ ./out/build/x64/test/Debug/magicTest.exe
Randomness seeded to: 317398127

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
magicTest.exe is a Catch2 v3.3.2 host application.
Run with -? for options

-------------------------------------------------------------------------------
magic tests
  delete this require and add your own tests!
-------------------------------------------------------------------------------
/<path to your repo>/foo/test/foo.tests.cpp(13)
...............................................................................

/<path to your repo>/foo/test/foo.tests.cpp(14): FAILED:
  REQUIRE( false )

===============================================================================
test cases: 1 | 1 failed
assertions: 1 | 1 failed
```
As you can see, the test failed. This is intentional. You're now ready to go! Go write your first test for the project that you're planning to make and have fun coding safely in your full devops environment :)

**A quick thing to note** is that the examples here are all on the command line, but you can totally just open the project in an IDE and work in there, if you like. You might need to set up some of the run configuration and parameters and whatnot, but it should be quite simple, as long as your chosen IDE understands CMake projects (or whatever build system you selected when creating the project).
### Push your changes
Once you've run `ccpstart`, then you will have a perfectly good repo to push to Github. You just need to make a new repo on Github and then follow the instructions to push an existing repo to it. Typically, this will involve adding a new remote that points to your repo and then pushing the changes to that repo.

So, say your name is Aisha Adeboye and you want to make a new project called "Weebles", and you already have a Github repo with an equivalent name, then you might do something like:
```shell
cppstart weebles
cd weebles
git remote add origin git@github.com:aishaadeboye/weebles.git
git push -u origin main
```
The way Github workflows work means that you won't generate any CI run on this first push, but the next one (and all the other ones after that) will.  This means that it's a good idea to get on with fixing the failing test by replacing it with one for some new code that you're writing; otherwise you'll get a test run failure on Github. How embarrassing!

## Releasing your code
There's a good chance that you're embarking on your project because you think other people might find its features useful in some way.  In that case, you'll probably want to create releases to distribute to other people. To do this, you should tag your repo with a tag like `v1.2.3`, or whatever release number you're on and push that tag. When Github sees that tag arrive in the repo, it will trigger the Release workflow and produce things like a zip file of the code and things. There's a VERY high chance that you'll need to tweak things to get them the way you want them for your project, but the basics are kind of there to get you going (which is the point of this project :) ).  So, to create and push a tag, go for something like this:
```shell
git tag v1.2.3
git push --tags
```
Then go trigger the "release" action on Github.

## All the options
You can configure the type of project that gets created with the following options:
```text
usage: cppstart [-h] [-A | -L]
                [-b BUILD_SYSTEM]
                [-c COPYRIGHT_NAME]
                [-d DEPENDENCY_MANAGEMENT]
                [-i CI]
                [-l LICENSE]
                [-o OUTPUT_DIRECTORY]
                [-s SOURCE_CONTROL]
                proj_name

positional arguments:
  proj_name             name of the project

options:
  -h, --help            show this help message and exit
  -A, --app             create an application project
  -L, --lib             create a library project
  -b BUILD_SYSTEM, --build-system BUILD_SYSTEM
                        the type of build system that the project is going to use. Valid options are:
                          - cmake
  -c COPYRIGHT_NAME, --copyright-name COPYRIGHT_NAME
                        name that will be used in copyright info
  -d DEPENDENCY_MANAGEMENT, --dependency-management DEPENDENCY_MANAGEMENT
                        the type of dependency manager that the project will use. Valid options are:
                          - conan
  -i CI, --ci CI        the type of CI system that the project will use. Valid options are:
                          - github
  -l , --license        the license that will be used in the project. Valid options are:
                          - AGPL-3.0-or-later,
                          - Apache-2.0,
                          - BSL-1.0,
                          - GPL-3.0-or-later,
                          - LGPL-3.0-or-later,
                          - MIT,
                          - MPL-2.0,
                          - Unlicense
  -o OUTPUT_DIRECTORY, --output-directory OUTPUT_DIRECTORY
                        output directory
  -s SOURCE_CONTROL, --source-control SOURCE_CONTROL
                        the type of source control that the project will use. Valid options are:
                          - git

```
You can see these options by doing `cppstart -h`.