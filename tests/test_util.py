# encoding: utf-8

from crank.util import *
from crank.util import _PY2

if _PY2:
    def u(s): return s.decode('utf-8')
else:
    def u(s): return s

def mock_f(self, a, b, c=None, d=50, *args, **kw):
    pass

def test_get_argspec_first_call():
    argspec = get_argspec(mock_f)
    assert argspec == (['a', 'b', 'c', 'd'], 'args', 'kw', (None, 50)), argspec

def test_get_argspec_cached():
    argspec = get_argspec(mock_f)
    assert argspec == (['a', 'b', 'c', 'd'], 'args', 'kw', (None, 50)), argspec

def test_get_params_with_argspec():
    params = get_params_with_argspec(mock_f, {'a':1, 'c':2}, [3])
    assert params == {'a': 3, 'c': 2}, params

def test_remove_argspec_params_from_params():
    params, remainder = remove_argspec_params_from_params(mock_f, {'a':1, 'b':2}, [3])
    assert params == {}, params
    assert remainder == (1, 2), repr(remainder)

def test_remove_argspec_params_from_params_remove_optional_positionals():
    params, remainder = remove_argspec_params_from_params(mock_f, {'c':45}, [3, 3, 4])
    assert params == {}, params
    assert remainder == (3, 3, 45), repr(remainder)

def test_remove_argspec_params_from_params_none_remainder():
    params, remainder = remove_argspec_params_from_params(mock_f, {'a':1, 'b':2}, None)
    assert params == {'a': 1, 'b': 2}, params
    assert remainder == None, repr(remainder)

def test_remove_argspec_params_from_params_none_param():
    params, remainder = remove_argspec_params_from_params(mock_f, {'b':None}, [3, 3])
    assert params == {}, params
    assert remainder == (3, None), repr(remainder)


def mock_f2(self, a, b):
    pass

def test_remove_argspec_params_from_params_in_remainder():
    params, remainder = remove_argspec_params_from_params(mock_f2, {'b':1}, ['a'])
    assert params == {}, params
    assert remainder == ('a', 1,), repr(remainder)


def test_remove_argspec_params_from_params_no_conditionals():
    params, remainder = remove_argspec_params_from_params(mock_f2, {'a':1, 'b':2}, ['a'])
    assert params == {}, params
    assert remainder == (1,2), repr(remainder)

def test_remove_argspec_params_from_params_req_var_in_params():
    params, remainder = remove_argspec_params_from_params(mock_f2, {'a':1, 'b':2}, ['a'])
    assert params == {}, params
    assert remainder == (1, 2), repr(remainder)

def test_remove_argspec_params_from_params_avoid_creating_duplicate_parameters():
    params, remainder = remove_argspec_params_from_params(mock_f, {'a':1, 'b':2, 'c':3}, ['a', 'b'])
    assert params == {'c': 3}, params
    assert remainder == (1, 2), repr(remainder)

def test_remove_argspec_params_from_params_avoid_duplicate_params():
    params, remainder = remove_argspec_params_from_params(mock_f2, {'a':1, 'b':2}, ['a', 'b'])


def assert_path(instance, expected, kind=list):
    assert kind(instance.path) == expected, (kind(instance.path), expected)

def test_path_path():
    assert Path(Path('/foo')) == ['', 'foo']

def test_path_list():
    class MockOb(object):
        path = Path()
    
    cases = [
            ('/', ['', '']),
            ('/foo', ['', 'foo']),
            ('/foo/bar', ['', 'foo', 'bar']),
            ('/foo/bar/', ['', 'foo', 'bar', '']),
            ('/foo//bar/', ['', 'foo', '', 'bar', '']),
            (('foo', ), ['foo']),
            (('foo', 'bar'), ['foo', 'bar'])
        ]
    
    for case, expected in cases:
        instance = MockOb()
        instance.path = case
        
        yield assert_path, instance, expected

def test_path_str():
    class MockOb(object):
        path = Path()
    
    cases = [
            ('/', "/"),
            ('/foo', '/foo'),
            ('/foo/bar', '/foo/bar'),
            ('/foo/bar/', '/foo/bar/'),
            ('/foo//bar/', '/foo//bar/'),
            (('foo', ), 'foo'),
            (('foo', 'bar'), 'foo/bar')
        ]
    
    for case, expected in cases:
        instance = MockOb()
        instance.path = case
        
        yield assert_path, instance, expected, str
    
    instance = MockOb()
    instance.path = '/foo/bar'
    yield assert_path, instance, """<Path "deque([\'\', \'foo\', \'bar\'])">""", repr

def test_path_unicode():
    class MockOb(object):
        path = Path()
    
    cases = [
            ('/', "/"),
            (u('/©'), u('/©')),
            (u('/©/™'), u('/©/™')),
            (u('/©/™/'), u('/©/™/')),
            ((u('¡'), ), u('¡')),
            (('foo', u('¡')), u('foo/¡'))
        ]
    
    for case, expected in cases:
        instance = MockOb()
        instance.path = case

        if _PY2:
            yield assert_path, instance, expected, unicode
        else:
            yield assert_path, instance, expected, str

def test_path_slicing():
    class MockOb(object):
        path = Path()
    
    instance = MockOb()
    
    instance.path = '/foo/bar/baz'
    
    assert str(instance.path[1:]) == 'foo/bar/baz'
    assert str(instance.path[2:]) == 'bar/baz'
    assert str(instance.path[0:2]) == '/foo'
    assert str(instance.path[::2]) == '/bar'

def test_path_comparison():
    assert Path('/foo') == ('', 'foo'), 'tuple comparison'
    assert Path('/foo') == ['', 'foo'], 'list comparison'
    assert Path('/foo') == '/foo', 'string comparison'
    assert Path(u('/föö')) == u('/föö'), 'string comparison'

def test_path_translation():
    translated = default_path_translator('a.b')
    assert translated == 'a_b', translated

    translated = default_path_translator(u('f.ö.ö'))
    assert translated == u('f_ö_ö'), translated
