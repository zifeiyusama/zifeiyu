import os
_basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True

ADMINS = frozenset(['youremail@yourdomain.com'])
SECRET_KEY = 'f2f49908291696b8a4bb7d36b83589995cdca626'

SQLALCHEMY_DATABASE_URI = 'postgres://zfjoxmtggitxte:KRrDVUAz0bt6WMpfMrzYPggmSx@ec2-54-83-198-111.compute-1.amazonaws.com:5432/dkiccm559kf32'
DATABASE_CONNECT_OPTIONS = {}


# THREADS_PER_PAGE = 8

WTF_CSRF_ENABLED = True
WTF_CSRF_SECRET_KEY = "8f37f2a475fc1cdcdb9496337244b760456f0646"


# RECAPTCHA_USE_SSL = False
# RECAPTCHA_PUBLIC_KEY = '6LeYIbsSAAAAACRPIllxA7wvXjIE411PfdB2gt2J'
# RECAPTCHA_PRIVATE_KEY = '6LeYIbsSAAAAAJezaIq3Ft_hSTo0YtyeFG-JgRtu'
# RECAPTCHA_OPTIONS = {'theme': 'white'}
