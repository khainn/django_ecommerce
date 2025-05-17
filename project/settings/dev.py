from project.settings.deploy import *  # noqa: F401, F403  # pylint: disable=wildcard-import,unused-wildcard-import

DEBUG = True

ALLOWED_HOSTS = ['*']

# Explicitly set the admin site URL for development
ADMIN_SITE_URL = 'https://dac-san-luc-ngan.vercel.app/'

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
NOSE_ARGS = [
    '--with-coverage',
    '--cover-erase',
    '--cover-xml-file=/tmp/coverage.xml',
    '--cover-xml',
    '--with-xunit',
    '--xunit-file=/tmp/xunittest.xml',
    '--cover-package=apps',
    '--cover-min-percentage=60',
]
