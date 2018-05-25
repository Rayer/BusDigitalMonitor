import utils.singleton
import unittest


class TestObject(metaclass=utils.singleton.Singleton):
    pass


class SingletonSanity(unittest.TestCase):
    def test_singleton_same_object_metaclass(self):
        a = TestObject()
        b = TestObject()
        self.assertEqual(a, b)
