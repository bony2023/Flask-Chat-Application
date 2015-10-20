#Bluemix Python Web application

This application is based on [Flask microframework](http://flask.pocoo.org/) and is intended to deploy on [IBM's Bluemix](https://bluemix.net/) environment which is based on Cloud Foundry.

IBM Bluemix contains the Python buildpack from [Cloud Foundry](https://github.com/cloudfoundry/python-buildpack) and so will be auto-detected as long as a requirements.txt or a run.py is located in the root of your application.

If you just wish to automatically deploy this application to Bluemix then just click the 'Deploy to Bluemix' button.

[![Deploy to Bluemix](https://bluemix.net/deploy/button.png)](https://bluemix.net/deploy?repository=https://github.com/bony2023/Flask-Chat-Application)