import asyncio
from grpc.aio import insecure_channel
from echo_pb2 import echoMessage
from echo_pb2_grpc import EchoServiceStub

clients = ['127.0.0.1','10.24.24.57','10.24.24.58']
r_clients = []

async def grpc_echo(client,channel):
    stub = EchoServiceStub(channel)
    print(f"Sending echo to {client}")
    response = await stub.Echo(echoMessage(text=f"{client} responded."))
    r_clients.append(response.text)

async def channel_generator(clients):
    for client in clients:
        channel = insecure_channel(f"{client}:50051")
        yield (client,channel)

async def main(clients):
    channel_list = []
    async for response in channel_generator(clients):
        channel_list.append(response)
    await asyncio.gather(*(grpc_echo(client,channel) for (client,channel) in channel_list))

if __name__ == "__main__":
    asyncio.run(main(clients))
    print(r_clients)
