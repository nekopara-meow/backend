# store some Secrets
class Secrets:
    class Email:
        emailHost = 'smtp.126.com'
        emailPort = 25
        emailAddr = 'couteau69586@126.com'
        emailPasswd = 'CVEPODZWIPRAMTPX'

    class RootUrl:
        Frontend = 'http://127.0.0.1:8080'
        Backend = 'http://127.0.0.1:8080'


class Settings:
    SECRET_KEY = 'django-insecure-j$25)6it^$87hp7x(9!khs#^3ng&u%cloka*kdotv*shpvm7y1'


class Database:
    ENGINE = 'django.db.backends.mysql'
    NAME = 'backend'
    USER = 'couteau69586'
    PASSWORD = 'Lhy69586'
    HOST = 'bj-cynosdbmysql-grp-lqndnpoe.sql.tencentcdb.com'
    PORT = '20789'
