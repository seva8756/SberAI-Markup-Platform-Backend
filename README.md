# SberAI-Markup-Platform-Backend

# Backend Setup Guide

This guide will walk you through setting up and running the backend for your project.

For the frontend repository, visit
[https://github.com/seva8756/SberAI-Markup-Platform-Frontend](https://github.com/seva8756/SberAI-Markup-Platform-Frontend)

## Prerequisites

- Make sure you have all necessary dependencies installed.

## Installation

1. Install dependencies:
    ```bash
    make install
    ```

## Database Setup

1. Create two databases: Main and Test.

## Configuration

1. Locate the `apiserver.toml` file and fill in the following fields:
    - **Database**: Fill in the details for your main database.
    - **TestDatabase**: Fill in the details for your test database.
    - **Alembic**: Specify the database you want to apply migrations to (name should match one of the above configurations).
    - **JWT_SECRET_KEY**: Set a secret key for JWT (for example you can use the following key):
        ```
        82d1df42arc7c08a55127f0061621be1c2d9a81e77a7f4d56fcn76d38075b60061621be1c2d9a81e77a7f
        ```

## Database Migration

1. Upgrade the database schema:
    ```bash
    make upgrade_db
    ```

2. To downgrade the database schema to the initial version:
    ```bash
    make downgrade_db
    ```

## Testing

1. Run tests to ensure everything is set up correctly:
    ```bash
    make test
    ```

## Running the Server

1. Start the server:
    ```bash
    make run
    ```

2. You can now access the server and start using the backend.
