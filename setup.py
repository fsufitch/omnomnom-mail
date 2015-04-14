from setuptools import setup, Extension, find_packages

setup(name='omnomnom',
      version='0.1',
      author='Filip Sufitchi',
      author_email="fsufitchi@gmail.com",
      description="Spam black hole",
      url="http://omnomnom.email",
      package_dir={'': 'src'},
      packages=find_packages('src'),
      include_package_data=True,
      entry_points = {'console_scripts': [
          "omnomnom_smtp=omnomnom.mailserv.server:main",
      ]},
      install_requires=['yaul', 'sqlalchemy'],
)
