from couchbase_tests.base import MockTestCase
from functools import wraps
from parameterized import parameterized_class
from collections import namedtuple

Details = namedtuple('Details', ['factory', 'get_value'])

try:
    from txcouchbase.bucket import Bucket
    from txcouchbase.bucket import Collection


    def asynct(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            return f(*args, **kwargs)

        return wrapper


    def gen_collection(*args, **kwargs):
        try:
            base_bucket = Bucket(*args, **kwargs)
            return base_bucket.default_collection()
        except Exception as e:
            raise

    default=Details(gen_collection, lambda x: x.content)
    target_dict = {'V3CoreClient': Details(Collection, lambda x: x.value),
                   'Collection': default}

except (ImportError, SyntaxError):
    target_dict = {}

targets = list(map(lambda x: (x,), target_dict.keys()))


def parameterize_twisted(cls):
    return parameterized_class(('factory_name',), targets)(cls)


class AioTestCase(MockTestCase):
    factory_name = None  # type: str

    def __init__(self, *args, **kwargs):
        self.details = target_dict.get(self.factory_name,default)
        self._factory = self.details.factory
        super(AioTestCase, self).__init__(*args, **kwargs)

    @property
    def factory(self):
        return self._factory

    @factory.setter
    def factory(self, item):
        raise RuntimeError("This shouldn't happen, trying to override {} with {}".format(str(self._factory), str(item)))


    should_check_refcount = False
