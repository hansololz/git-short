from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
  long_description = fh.read()

setup(
  name="git-short",
  version="1.0.1",
  author="David Zhang",
  author_email="david.zhang.han@gmail.com",
  description="CLI commands to help using git more convenient.",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/hansololz/git-short",
  packages=find_packages(),
  classifiers=[
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3.7",
  ],
  python_requires=">=3.7",
  install_requires=[
    "click>=8.0.0",
  ],
  entry_points={
    "console_scripts": [
      "gsave=tools.cli:gsave",
      "gpush=tools.cli:gpush",
      "gsquash=tools.cli:gsquash",
      "gstash=tools.cli:gstash",
      "gpop=tools.cli:gpop",
      "gclear=tools.cli:gclear",
      "greset=tools.cli:greset",
      "gpull=tools.cli:gpull",
    ],
  },
)
