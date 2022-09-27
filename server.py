#  coding: utf-8 
import socketserver

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


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):

        self.data = self.request.recv(1024).strip()
        split_data = self.data.decode().split()
        
        if len(split_data) < 1: # check for empty requests
            self.request.sendall(bytearray("HTTP/1.1 404 Not Found\r\n\r\n",'utf-8'))
            return
   
        # splits request into a list of strings
        method = split_data[0] 

        # First argument should contain http method, check for GET
        if method != 'GET':
            self.request.sendall(bytearray("HTTP/1.1 405 Method Not Allowed\r\n\r\n",'utf-8'))
            return

        else: # get request received

            path = split_data[1] # get path

            # prevent user from accessing root directory
            if '../' in path:
                self.request.sendall(bytearray("HTTP/1.1 404 Not Found\r\n\r\n",'utf-8'))
                return

            # check if it's html, css or none
            path_ending = path.split('.')

            if path[-1] == '/': #return corresponding redirected html page
                path = path + 'index.html'
                self.get_html(path)
            elif path_ending[-1] == 'css': # gets request css file
                self.get_css(path)
            elif path_ending[-1] == 'html': # gets requested html file
                self.get_html(path)
            else:
                # path does not end in a valid file or path that ends with /
                # try to redirect, could be an invalid path
                self.redirect_page(path)


            

    def get_html(self, path):
        # retrieves of one of the index.html files
        # is_deep tells us whether we are using index.html in the deep folder or not
        file_name = 'www' + path

        try: #opens the html 
            file = open(file_name)
            content = file.read()
            file.close()

            self.request.sendall(bytearray("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n",'utf-8'))
            self.request.sendall(bytearray(content,'utf-8'))
            
        except:
            self.request.sendall(bytearray("HTTP/1.1 404 Not Found\r\n\r\n",'utf-8'))
            return
        return

    def get_css(self, path):
        # retrieves of a css file
        file_name = 'www' + path

        try: #opens the html 
            file = open(file_name)
            content = file.read()
            file.close()

            self.request.sendall(bytearray("HTTP/1.1 200 OK\r\nContent-Type: text/css\r\n\r\n",'utf-8'))
            self.request.sendall(bytearray(content,'utf-8'))
            
        except:
            self.request.sendall(bytearray("HTTP/1.1 404 Not Found\r\n\r\n",'utf-8'))
            return
        return

    def redirect_page(self, path):
        # assuming user is trying go to existing directory with incorrect path
        file_name = 'www' + path + '/index.html' 
        base_url = "http://127.0.0.1:8080"

        try: # tries to enter the correct directory, check if it exists
            file = open(file_name)
            content = file.read()
            file.close()

            self.request.sendall(bytearray("HTTP/1.1 301 Moved Permanently\r\nLocation: " + base_url + path + '/' + "\r\n\r\n",'utf-8'))
            #self.request.sendall(bytearray(content,'utf-8'))
            
        except: # the requested path does not exist at all
            self.request.sendall(bytearray("HTTP/1.1 404 Not Found\r\n\r\n",'utf-8'))
            return
        return
    
    
        
        

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
