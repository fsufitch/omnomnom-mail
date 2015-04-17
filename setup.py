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
          "omnomnom_smtpd=omnomnom.mailserv.server:service_main",
          "omnomnom_webui=omnomnom.webui.server:main",
          "omnomnom_webuid=omnomnom.webui.server:service_main",
      ]},
      install_requires=['pymysql', 'yaul', 'sqlalchemy', 'tornado', 'jinja2'],
)
