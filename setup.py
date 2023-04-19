from setuptools import setup, find_packages

setup(
    name="cppstart",
    version="1.0.0",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "cppstart = cppstart.main:main"
        ]
    },
    install_requires=["appdirs", "gitpython"],
    include_package_data=True
)
