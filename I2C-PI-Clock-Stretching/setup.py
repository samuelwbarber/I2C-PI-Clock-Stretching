from setuptools import setup, find_packages

setup(
    name="I2C-PI-Clock-Stretching",
    version="0.1",
    packages=find_packages(),
    install_requires=["RPi.GPIO"],  
    author="Sam Barber",
    description="A Raspberry Pi library for interfacing with I2C devices that use clock stretching. Bypassing the hardware flaw in the built in I2C itnerface.",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
    ],
)
