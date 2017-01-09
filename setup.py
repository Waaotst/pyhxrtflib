from setuptools import setup, find_packages

setup(
    name = 'tkpyhxrtflib',
    version='0.0.1',
    description = 'text plugin - easily save and load multiple font styles',
    url = 'https://github.com/nudebandage/tkpyhxrtflib',
    author='timothy eichler',
    author_email='tim_eichler@hotmail.com',
    license='BSD',
    classifiers=[
            'Development Status :: 3 - Alpha',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: BSD License',
            'Programming Language :: Python :: 3',
    ],

    # What does your project relate to?
    keywords = 'text font style bold underline italic color hxrtflib',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
)

#https://hynek.me/articles/sharing-your-labor-of-love-pypi-quick-and-dirty/
# python setup.py sdist bdist_wheel
# python setup.py sdist upload
# python setup.py bdist_wheel upload
