# Socket Programming Chat Application

## Overview

This repository contains the implementation of a client-server communication application built using Python. The application allows multiple clients to connect to a server and exchange messages in real-time. It includes features such as client naming, message acknowledgment, and connection management.

## Features

- **TCP Communication**: Utilizes TCP sockets for reliable communication.
- **Client Naming**: Clients are assigned unique names (e.g., Client01, Client02).
- **Message Exchange**: Clients can send messages to the server, which echoes back with "ACK".
- **Connection Status**: Clients can request the server for the list of active connections.
- **File Management**: Clients can request a list of files stored on the server and download them.

## Getting Started

### Prerequisites

- Python 3.x

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/TrueCodee/Socket-Programming-Chat-Application.git
   
2. Navigate to the project directory
   cd /Socket-Programming-Chat-Application

## Running Application
1. Start the server:
- python server.py

2. Open multiple terminal windows or tabs and start the clients:
- python client.py

## Usage

- Clients will be automatically named upon connection.
- To send messages to the server:
  - Type your message and press Enter.
  - The server will respond with an acknowledgment ("ACK").
- To view the current connections:
  - Type `status` and press Enter.
- To view items in the list:
  - Type print [filename] to request a specific file from the server.
- To close the client connection:
  - Type `exit` and press Enter.

## License
This project is licensed under the MIT License - see the LICENSE file for details.
