# Gym Assistant

## Overview

Gym Assistant is an AI-powered web application designed to offer personalized fitness guidance and health tracking. It provides users with workout plans, nutrition recommendations, and real-time monitoring based on fitness goals and health data. The app integrates with wearable devices and third-party APIs to deliver a comprehensive fitness and wellness experience.

## Features

- **Personalized Workout Plans**: Custom workouts based on individual goals and fitness levels.
- **Nutritional Recommendations**: Meal suggestions that cater to dietary restrictions and health objectives.
- **Real-Time Health Monitoring**: Monitors health metrics such as heart rate, sleep, and activity levels.
- **Integration with Wearables**: Sync data from fitness devices for comprehensive health insights.
- **Location-Based Suggestions**: Recommends local gyms and fitness centers based on user’s location.
- **Reminder System**: Notifications for workouts, meals, and health alerts.

## Tech Stack

- **Backend**: [FastAPI](https://fastapi.tiangolo.com/) - a modern web framework for building APIs with Python.
- **Frontend**: [React.js](https://reactjs.org/) - a JavaScript library for creating user interfaces.
- **Database**: [PostgreSQL](https://www.postgresql.org/) - for reliable, robust data storage.
- **AI and Data Processing**: Integration with [MyFitnessPal](https://www.myfitnesspal.com/) API, USDA nutrition data, and custom AI models.
- **Health & Fitness Data Integration**: API support for wearables like Fitbit, Garmin, and Apple Health.
- **CI/CD**: Continuous integration and deployment using GitHub Actions.
- **Containerization**: [Docker](https://www.docker.com/) for consistent environment and deployment.
- **Authentication**: OAuth 2.0 for secure user login.

## Project Structure

```plaintext
├── backend/
│   ├── app/               # FastAPI application
│   ├── tests/             # Unit and integration tests
│   └── Dockerfile         # Dockerfile for backend
├── frontend/
│   ├── public/            # Public assets
│   ├── src/               # React components and services
│   └── Dockerfile         # Dockerfile for frontend
├── .github/               # GitHub Actions CI/CD configurations
└── README.md              # Project documentation
