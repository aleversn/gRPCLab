# %%
import grpc
import basic_pb2
import basic_pb2_grpc
from tqdm import tqdm

# %%
def run():
    channel = grpc.insecure_channel('localhost:8080')

    stub = basic_pb2_grpc.TestStub(channel)
    response = stub.SetUserInfo(basic_pb2.UserInfo(userid='lpc1290', name='lpc', pwd='123456'))
    print('SetUserInfo Return: {}'.format(response))
    response = stub.GetUserInfo(basic_pb2.UserInfo(userid='lpc1290', name='lpc', pwd='123456'))
    print('GetUserInfo Return: {}'.format(response))

if __name__ == '__main__':
    run()

# %%
def sendfile():
    channel = grpc.insecure_channel('localhost:8080')

    stub = basic_pb2_grpc.FileStub(channel)
    def readfile():
        with open('1.jpg', 'rb') as f:
            lines = f.readlines()
            for line in tqdm(lines):
                yield basic_pb2.Image(img=line)
    response = stub.SetImage(readfile())
    print('SetUserInfo Return: {}'.format(response))

sendfile()

# %%
def getfile(filename):
    channel = grpc.insecure_channel('localhost:8080')

    stub = basic_pb2_grpc.FileStub(channel)
    response = stub.GetImage(basic_pb2.UserInfo(userid=filename))
    with open('get_{}'.format(filename), 'ab') as f:
        for r in tqdm(response):
            f.write(r.img)

getfile('1.jpg')

# %%
