import requests

from classes.login import Login
from classes.logger import logger
log = logger().log

with open('config/accounts.txt') as accounts_file:
    accounts = accounts_file.read().splitlines()


def run(x):
    req = requests.Session()

    log("{} Attempting Login".format(x.split(':')[0]))
    l = Login(req)
    l.login(x)

for x in accounts:
    run(x)