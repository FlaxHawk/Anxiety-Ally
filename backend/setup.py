from setuptools import setup, find_packages

setup(
    name="anxiety-ally-api",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        line.strip()
        for line in open("requirements.txt").readlines()
        if not line.startswith("#")
    ],
    author="Anxiety Ally Team",
    author_email="info@anxiety-ally.com",
    description="Backend API for Anxiety Ally mental health platform",
    keywords="anxiety, mental health, therapy, fastapi",
    python_requires=">=3.9",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Healthcare Industry",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
) 