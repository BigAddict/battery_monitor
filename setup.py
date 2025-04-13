from setuptools import setup, find_packages

setup(
    name="battery_monitor",
    version="0.2.0",
    packages=find_packages(),
    install_requires=[
        "psutil>=5.9.0",
    ],
    extras_require={
        "windows": ["win10toast>=0.9"],
    },
    entry_points={
        "console_scripts": [
            "battery-monitor=battery_monitor:main",
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="A utility to monitor laptop battery and alert when below a configurable threshold",
    keywords="battery, monitor, alert, laptop, notification",
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Utilities",
    ],
)
