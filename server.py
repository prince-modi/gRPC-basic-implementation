from concurrent import futures
import grpc
import time
import echo_pb2, echo_pb2_grpc

class Echo(echo_pb2_grpc.EchoService):

    def Echo(self, request, context):
        time.sleep(10)
        return echo_pb2.echoMessage(text=f"Echo echo echo {request.text}")

def serve():
    sync_server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    echo_pb2_grpc.add_EchoServiceServicer_to_server(Echo(),sync_server)
    sync_server.add_insecure_port('[::]:50051')
    sync_server.start()
    sync_server.wait_for_termination()

if __name__ == "__main__":
    serve()
