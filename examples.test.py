import uasyncio as asyncio
from microtest import expect, test, run, spy, async_spy

@test
async def one_and_one_should_be_added():
  expect(1 + 1).to_be(2)

@test
async def arrays_should_be_deep_compared():
  expect([1, 's', ('tuple'), {"a": 1}]).to_be([1, 's', ('tuple'), {"a": 1}])
  expect([{"a": 1}]).it_not().to_be([{"a": 2}])

@test
async def it_should_not_have_called_the_spy():
  spy_instance = spy()
  expect(spy_instance).it_not().to_have_been_called()

@test
async def spies_should_be_called():
  spy_instance = spy()
  spy_instance()
  spy_instance()
  expect(spy_instance).to_have_been_called()
  expect(spy_instance).it_not().to_have_been_called_times(1)
  expect(spy_instance).to_have_been_called_times(2)

@test
async def spies_should_be_called_with_args():
  spy_one = spy()
  spy_two = spy()
  spy_one(1)
  spy_two(1, 2)
  expect(spy_one).to_have_been_called_with(1)
  expect(spy_two).to_have_been_called_with(1, 2)
  expect(spy_two).it_not().to_have_been_called_with(10)

@test
async def spy_should_return_value_that_was_set():
  spy_one = spy().returns(10)
  expect(spy_one()).to_be(10)

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
  await asyncio.sleep(1)
  return 'it works!'

@test
async def test_should_await():
  expect(await job()).to_be('it works!')

run()