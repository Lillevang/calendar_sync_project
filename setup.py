from setuptools import setup, find_packages

setup(
    name="calendar_sync",
    version="0.1.0",
    author="Jeppe Lillevang Salling",
    author_email="jeppe.lillevang@gmail.com",
    description="A CLI tool for syncing and managing calendar events between calendars",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Lillevang/calendar_sync_project",
    packages=find_packages(),  # Automatically find the packages in your project
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",  # Ensure the project uses Python 3.6 or higher
    install_requires=[
        "click",  # Command line interface
        "icalendar",  # For working with ICS files
    ],
    entry_points={
        "console_scripts": [
            "calendar-sync=sync_calendars:cli",  # Command line entry point for your app
        ],
    },
)
