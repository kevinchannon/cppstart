from setuptools import setup, find_packages
import packaging.version

print(dir(packaging.version))

setup(
    name="cppstart",
    version=packaging.version.number,
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "cppstart = cppstart.main:main"
        ]
    },
    install_requires=["appdirs", "gitpython"],
    include_package_data=True
)
