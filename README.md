# cs262-DE1
A simple chat application made for the first design exercise of CS 262.

See https://docs.google.com/document/d/1PBET1TfQYQyCYWUZmwDo1rPKemiwzmbXX_95g0_28sA/edit?usp=sharing for detailed engineering notebook.

## Required Libraries/Versions
Necessary packages:
- Python 3.10 (conda install python=3.10.9) - needed because of the match statements
- socket
- _thread
- threading
- re
- sys
- select
- conda install grpcio
- conda install protobuf

## Instructions
### Custom Wire Protocol (Sockets)
at the root directory, run:
- "python3 server.py [host ip]" to get the server up, kill with control c
- in a different terminal window, run "python3 client.py [server host ip]" to get a client up, can follow instructions to exit cleanly or control c
- for testing, run "./test.sh" - if you don't see any messages stating that a client failed, all tests have passed - if permission denied when running, run chmod a+rx test.sh

### gRPC
in the "grpc_implementation" directory, run:
- "python3 server.py [host ip]" to get the server up, kill with control c
- in a different terminal window, run "python3 client.py [server host ip]" to get a client up, can follow instructions to exit cleanly or control c
- for testing, run "./grpc_test.sh" - if you don't see any messages stating that a client failed, all tests have passed - if permission denied when running, run chmod a+rx grpc_test.sh - may see a gRPC Channel closed message, which is perfectly fine (happens when the bash script controls c the server at end of tests)