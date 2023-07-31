import setuptools

# Get requirements from requirements.txt, stripping the version tags
with open('requirements.txt') as f:
    requires = [
        r.split('/')[-1] if r.startswith('git+') else r
        for r in f.read().splitlines()]

with open('README.md') as file:
    readme = file.read()

setuptools.setup(name='legend_plot_style',
                 version='0.0.1',
                 description='plot settings for LEGEND',
                 author='LEGEND collaboration',
                 url='https://github.com/legend-exp/legend_plot_style',
                 long_description=readme,
                 long_description_content_type="text/markdown",
                 setup_requires=['pytest-runner'],
                 install_requires=requires,
                 tests_require=requires + [
                     'pytest',
                 ],
                 python_requires=">=3.6",
                 packages=setuptools.find_packages(),
                 scripts=[],
                 classifiers=[
                     'Development Status :: 4 - Beta',
                     'License :: OSI Approved :: BSD License',
                     'Natural Language :: English',
                     'Programming Language :: Python :: 3.6',
                     'Intended Audience :: Science/Research',
                     'Programming Language :: Python :: Implementation :: CPython',
                     'Topic :: Scientific/Engineering :: Physics',
                 ],
                 zip_safe=False)
