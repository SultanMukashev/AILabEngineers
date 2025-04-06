FROM debian:bullseye

# Install g++, PostgreSQL client tools (includes pg_isready), and libpqxx
RUN apt update && apt install -y g++ libpqxx-dev libpq-dev postgresql-client

WORKDIR /app

# Copy everything into the container
COPY . .

# Compile the C++ app
RUN g++ load_postgres.cpp -o app -lpqxx -lpq

# Make the wait script executable
RUN chmod +x /app/wait-for-postgres.sh

# Run the wait script before starting the app
CMD ["./wait-for-postgres.sh"]