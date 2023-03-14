class Expect:
  def __init__(self, value):
    self.value = value
    self._not = False

  def it_not(self):
    self._not = True
    return self

  def evaluate(self, value):
    return not value if self._not else value

  def not_text(self):
    return 'not ' if self._not else ''

  def to_be(self, expected):
    if (self.evaluate(self.value != expected)):
      raise Exception('Expected: {}{}\nReceived: {}'.format(self.not_text(), expected, self.value))

  def to_have_been_called(self):
    if (self.evaluate(len(self.value.calls) == 0)):
      raise Exception('Expected spy to {}be called.'.format(self.not_text()))

  def to_have_been_called_with(self, *expected):
    has_expected = False

    for arg in self.value.calls:
      has_expected = arg == expected
      if (has_expected):
        break

    if (self.evaluate(not has_expected)):
      raise Exception('Expected spy to {}have been called with {}.'.format(self.not_text(), expected))

  def to_have_been_called_times(self, expected):
    count = len(self.value.calls)
    if (self.evaluate(count != expected)):
      raise Exception('Expected spy to {}be called {} times. It was called {} times.'.format(self.not_text(), expected, count))

class Spy:
  def __init__(self):
    self.return_value = None
    self.calls = []

  def returns(self, value):
    self.return_value = value
    return self

  def __call__(self, *args):
    self.calls.append(args)
    return self.return_value

class AsyncSpy(Spy):
  async def __call__(self, *args):
    self.calls.append(args)
    return self.return_value

def spy():
  return Spy()

def async_spy():
  return AsyncSpy()

def expect(value):
    return Expect(value)

async def test(*functions):
  print('------------------------------------------------')

  for test_function in functions:
    name = test_function.__name__.replace("_", " ")

    try:
      await test_function()
      print('PASS', name)
    except Exception as e:
      print('FAIL', name)
      print(e)
  
  print('------------------------------------------------')
