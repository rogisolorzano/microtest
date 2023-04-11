import uasyncio
from microtest import expect, test, run, spy, async_spy, observe, mock_module

@test
async def one_and_one_should_be_added():
  expect(1 + 1).to_be(2)

@test
async def arrays_should_be_deep_compared():
  expect([1, 's', ('tuple'), {"a": 1}]).to_be([1, 's', ('tuple'), {"a": 1}])
  expect([{"a": 1}]).it_not.to_be([{"a": 2}])

@test
async def it_should_not_have_called_the_spy():
  spy_instance = spy()
  expect(spy_instance).it_not.to_have_been_called()

@test
async def spies_should_be_called():
  spy_instance = spy()
  spy_instance()
  spy_instance()
  expect(spy_instance).to_have_been_called()
  expect(spy_instance).it_not.to_have_been_called_times(1)
  expect(spy_instance).to_have_been_called_times(2)

@test
async def spies_should_be_called_with_args():
  spy_one = spy()
  spy_two = spy()
  spy_one(1)
  spy_two(1, 2)
  expect(spy_one).to_have_been_called_with(1)
  expect(spy_two).to_have_been_called_with(1, 2)
  expect(spy_two).it_not.to_have_been_called_with(10)

@test
async def spies_should_handle_keyword_args():
  spy_one = spy()
  spy_two = spy()
  spy_one(example = True, timeout = 10)
  spy_one(example = False, timeout = 30)
  spy_two(1, param = 2)
  expect(spy_one).to_have_been_called_with(example = True, timeout = 10)
  expect(spy_two).to_have_been_called_with(1, param = 2)

@test
async def spy_should_return_value_that_was_set():
  spy_one = spy().returns(10)
  expect(spy_one()).to_be(10)

@test
async def spy_should_return_values_set_in_order_then_only_single_returns_value():
  spy_one = spy().define_returns(10, 20, 30)
  spy_one.returns(100)
  expect(spy_one()).to_be(10)
  expect(spy_one()).to_be(20)
  expect(spy_one()).to_be(30)
  expect(spy_one()).to_be(100)
  expect(spy_one()).to_be(100)
  expect(spy_one()).to_be(100)

@test
async def it_should_catch_async_exception():
  async def boom():
    await uasyncio.sleep_ms(500)
    raise Exception("Boom")
  
  await expect(boom).to_throw()

class CustomException(Exception):
  pass

class OtherException(Exception):
  pass

@test
async def it_should_catch_custom_exception():
  async def boom():
    await uasyncio.sleep_ms(500)
    raise CustomException("Boom")
  
  await expect(boom).to_throw(CustomException)

@test
async def it_should_not_catch_other_exception():
  async def boom():
    await uasyncio.sleep_ms(500)
    raise CustomException("Boom")
  
  await expect(boom).it_not.to_throw(OtherException)

@test
async def it_should_observe_event():
  event = uasyncio.Event()
  observer = observe(event)

  expect(observer).it_not.to_have_been_triggered()

  event.set()
  await observer.wait()

  expect(observer).to_have_been_triggered()

class NetworkMock:
  def __init__(self):
    self.hostname = spy()

network_mock = NetworkMock()
mock_module('network', network_mock)

from network import hostname

@test
async def it_should_mock_network_module():
  hostname()

  expect(network_mock.hostname).to_have_been_called_times(1)


class MockPublisher:
  def __init__(self):
    self.publish = async_spy()

class ExampleService:
  def __init__(self, publisher):
    self.publisher = publisher

  async def publish(self):
    await self.publisher.publish('message')

@test
async def example_service_should_publish_the_message():
  mock_publisher = MockPublisher()
  service = ExampleService(mock_publisher)

  await service.publish()

  expect(mock_publisher.publish).to_have_been_called()
  expect(mock_publisher.publish).to_have_been_called_with('message')

async def job():
  await uasyncio.sleep(1)
  return 'it works!'

@test
async def test_should_await():
  expect(await job()).to_be('it works!')

run()