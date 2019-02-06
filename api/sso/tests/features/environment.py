import os

from behave import fixture, use_fixture

from sso_api.api import sso
from selene.account import AccountRepository
from selene.util.db import get_db_connection


@fixture
def sso_client(context):
    sso.testing = True
    context.db_pool = sso.config['DB_CONNECTION_POOL']
    context.client_config = sso.config
    context.client = sso.test_client()

    yield context.client


def before_feature(context, _):
    use_fixture(sso_client, context)
    os.environ['SALT'] = 'testsalt'
    with get_db_connection(context.db_pool) as db:
        acct_repository = AccountRepository(db)
        account = acct_repository.add('foo@mycroft.ai', 'foo')

    context.account = account


def after_feature(context, _):
    with get_db_connection(context.db_pool) as db:
        acct_repository = AccountRepository(db)
        acct_repository.remove(context.account)
