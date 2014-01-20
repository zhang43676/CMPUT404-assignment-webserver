import SocketServer, os
# coding: utf-8

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(SocketServer.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        new_request = self.data.split()
        url = new_request[1]
        #denfense the hack!
        if "../" in url:
            self.request.sendall("HTTP/1.1 404 Bad Request\n")
            return
        #check the url
        if url == '/':
            new_file = os.getcwd() + "/www/index.html"    
        elif url[0] == '/' and url[-1] == '/':
            new_file = os.getcwd() + "/www" + url + "index.html"
        else:
            new_file = os.getcwd() + "/www" + url
        local_path = os.path.normpath(new_file)
        #get the content of page
        try:
            read_file = open(local_path, "r")
            content_type = new_file.split(".")[-1]
        #make a header
            http_header = "HTTP/1.1 200 OK\r\n" + "Content-Type: text/" + content_type + "; charset=UTF-8\r\n"
        #make the body
            http_content = read_file.read()
            http_content_len = "Content-Length:" +str(len(http_content)) + "\n"
            read_file.close()
        #if path is invalid, return 404 not found
        except IOError:
            http_header = "HTTP/1.1 404 Not Found\n"
            http_content = "\n"
            http_content_len = "Content-Length: 0 \n"
        #send the request
        self.request.sendall(http_header)
        self.request.sendall("\r\n")
        self.request.sendall(http_content+http_content_len)
                
        
        

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
