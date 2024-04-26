# FastAPI with Redis Pub/Sub and WebSocket

This project demonstrates the use of FastAPI with Redis for implementing publish-subscribe messaging patterns and WebSockets for real-time communication. It uses SQLite as the database for data persistence and is fully dockerized for easy setup and deployment.

## Prerequisites

- **Docker**: The project is containerized with Docker. Ensure Docker and Docker Compose are installed on your system. Download and install Docker from [Docker's official site](https://docs.docker.com/get-docker/).

## Project Components

- **FastAPI Application**: A Python web framework for building APIs with Python 3.9+ based on standard Python type hints.
- **Redis**: An in-memory data structure store, used as a database, cache, and message broker, here it is used for pub/sub messaging.
- **SQLite**: A C-language library that implements a small, fast, self-contained, high-reliability, full-featured, SQL database engine.
- **WebSockets**: Enables real-time bidirectional communication between the clients and the server.

## Setup and Installation

### Clone the repository

To get started, clone the repository to your local machine:

```bash
git clone https://github.com/yourusername/your-repository-name.git
cd your-repository-name
```

### Build and Run

To build and run the application using Docker Compose:

```bash
docker-compose up --build -d
```

This command builds the images and starts the services as defined in `docker-compose.yml`.

## Using the Application

Once the application is running, you can access the FastAPI app at:

```
http://localhost:8000
```

Redis will be running and accessible to the FastAPI app for pub/sub messaging. You can interact with the API using tools like curl, Postman, or any HTTP client.

## Testing WebSockets

You can test the WebSocket functionality using a WebSocket client or by writing a simple client script in JavaScript:

```javascript
const ws = new WebSocket("ws://localhost:8000/messaging/{group_id}/{user_id}");

ws.onmessage = function(event) {
  console.log('Received:', event.data);
};

ws.onopen = function(event) {
  ws.send('Hello Server!');
};
```

Replace `{group_id}` and `{user_id}` with appropriate values corresponding to your application logic.

## Shutting Down

To stop and remove the containers:

```bash
docker-compose down
```

