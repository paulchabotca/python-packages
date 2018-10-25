from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name="tlwanstatus",
    version="0.0.1",
    author="Paul Chabot",
    author_email="email@paulchabot.ca",
    description="Retrieves status of wan device on a TP-Link TD-W9970",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/paulchabotca/tlwanstatus",
    py_modules=['tplwanstatus'],
    packages=['tplwanstatus'],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'Click',
        'BeautifulSoup4',
        'Selenium',
        'Python-Dotenv',
    ],
    entry_points='''
        [console_scripts]
        tplwanstat=tplwanstatus.wanstatus:main
    ''',
)
