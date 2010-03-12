from crank.dispatchstate import DispatchState

class MockRequest(object):
    path_info = 'something'
    params = {'c':3, 'd':4}

class MockController(object):
    pass

class TestDispatchState:

    def setup(self):
        self.request = MockRequest()
        self.state = DispatchState(self.request, {'a':1, 'b':2})

    def test_create(self):
        assert self.state.params == {'a':1, 'b':2}, self.state.params

    def test_create_params_in_request(self):
        state = DispatchState(self.request)
        assert state.params == {'c':3, 'd':4}, state.params

    def test_add_controller(self):
        mock = MockController()
        self.state.add_controller('mock', mock)
        assert self.state.controller_path['mock'] == mock

    def test_add_method(self):
        self.state.add_method('a', 'b')
        assert self.state.method == 'a'
        assert self.state.remainder == 'b'

    def test_add_routing_args(self):
        current_path = 'current'
        remainder = ['c', 'd']
        fixed = ['e', 'f', 'g']
        var_args = ['g', 'h']
        self.state.add_routing_args(current_path, remainder, fixed, var_args)

    def test_controller(self):
        mock = MockController()
        self.state.add_controller('mock', mock)
        assert self.state.controller == mock
