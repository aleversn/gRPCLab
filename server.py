# %%
from concurrent import futures
import time
import grpc
import json
import basic_pb2
import basic_pb2_grpc

# %%
class Test(basic_pb2_grpc.TestServicer):

    def SetUserInfo(self, request, context):
        return basic_pb2.Status(code='200', status='success', info=request.userid)
    
    def GetUserInfo(self, request, context):
        return basic_pb2.UserInfo(userid=request.userid, name=request.name, pwd=request.pwd)

class File(basic_pb2_grpc.FileServicer):

    def SetImage(self, request, context):
        with open('2.jpg', 'ab') as f:
            for r in request:
                f.write(r.img)
        return basic_pb2.Status(code="200", status="success")
    
    def GetImage(self, request, context):
        filename = request.userid
        with open(filename, 'rb') as f:
            lines = f.readlines()
        for line in lines:
            yield basic_pb2.Image(img=line)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    basic_pb2_grpc.add_TestServicer_to_server(Test(), server)
    basic_pb2_grpc.add_FileServicer_to_server(File(), server)
    server.add_insecure_port('[::]:8080')
    server.start()

    try:
        while True:
            time.sleep(60*60*24)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()

# %%
