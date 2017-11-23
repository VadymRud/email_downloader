from distutils.core import setup

setup(name="mailtransfer",
      version="0.1",
      description="Mail dounloader/uploader",
      author="Vadym Rud",
      author_email="vadymrud1980@gmail.com",
      url="https://github.com/VadymRud/email_downloader",
    #Name the folder where your packages live:
    #(If you have other packages (dirs) or modules (py files) then
    #put them into the package directory - they will be found
    #recursively.)
      packages=['mailtransfer'],
    #'package' package must contain files (see list above)
    #I called the package 'package' thus cleverly confusing the whole issue...
    #This dict maps the package name =to=> directories
    #It says, package *needs* these files.
     # package_data={'package' : files },
    #'runner' is in the root.
      scripts=["runner"],
      long_description="""Really long text here."""
    #
    #This next part it for the Cheese Shop, look a little down the page.
    #classifiers=[]
)
