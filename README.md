# NEO Hazardous Classification 🚀

A machine learning application for classifying Near Earth Objects (NEOs) as potentially hazardous or not, built with FastAPI and Streamlit.

## 🌟 Features

- **FastAPI Backend**: RESTful API for hazard predictions
- **Streamlit Frontend**: Interactive web interface for user-friendly predictions
- **Machine Learning Model**: Trained classifier for NEO hazard assessment
- **Dockerized Deployment**: Easy setup and deployment using Docker

## 🏗️ Architecture

The application consists of two main components:
- **FastAPI API** (Port 8000): Provides prediction endpoints
- **Streamlit App** (Port 8503): User interface for interactive predictions

## 🛠️ Setup and Installation

### Prerequisites

- Docker installed on your system
- `.env` file with necessary environment variables

### Environment Setup

Create a `.env` file in the root directory with the following variables:
```
PORT=8000
# Add other environment variables as needed
```

### Building and Running with Docker

1. **Build the Docker image:**
```bash
docker build -t neo-hazardous-classification:neo .
```

2. **Run the container:**
```bash
docker run -d --env-file ./.env -p 8501:8503 -p 8000:8000 --name neo_classification neo-hazardous-classification:neo
```

### Alternative Single Port Setup (Recommended)

If you want to access only the Streamlit interface (which can communicate with the internal FastAPI):
```bash
docker run -d --env-file ./.env -p 8501:8503 --name neo_classification neo-hazardous-classification:neo
```

## 🚀 Usage

### Accessing the Application

- **Streamlit Web Interface**: http://localhost:8501
- **FastAPI Documentation** (if port 8000 is exposed): http://localhost:8000/docs
- **FastAPI Endpoints** (if port 8000 is exposed): http://localhost:8000

### Making Predictions

#### Via Streamlit Interface
1. Open http://localhost:8501 in your browser
2. Enter the required parameters:
   - Absolute Magnitude
   - Estimated Diameter (minimum)
   - Relative Velocity
   - Miss Distance
3. Click predict to get the hazard classification

#### Via API (if port 8000 is exposed)
Make a GET request to the prediction endpoint:
```bash
curl "http://localhost:8000/prediction?absolute_magnitude=20.5&estimated_diameter_min=0.1&relative_velocity=15000&miss_distance=5000000"
```

## 📊 Data

The application uses NASA's Near Earth Objects dataset (1910-2024), which is automatically downloaded during the Docker build process.

## 🔧 Container Management

### View running containers:
```bash
docker ps
```

### Stop the container:
```bash
docker stop neo_classification
```

### Remove the container:
```bash
docker rm neo_classification
```

### View container logs:
```bash
docker logs neo_classification
```

### Remove the image (optional):
```bash
docker rmi neo-hazardous-classification:neo
```

## 🐛 Troubleshooting

### Common Issues

1. **Port conflicts**: If port 8501 or 8000 is already in use, change the port mapping:
   ```bash
   docker run -d --env-file ./.env -p 8502:8503 --name neo_classification neo-hazardous-classification:neo
   ```

2. **Environment file not found**: Ensure `.env` file exists in the same directory as the Dockerfile

3. **Container fails to start**: Check logs using `docker logs neo_classification`

### Rebuilding after changes
If you make changes to the code, rebuild the image:
```bash
docker stop neo_classification
docker rm neo_classification
docker build -t neo-hazardous-classification:neo .
docker run -d --env-file ./.env -p 8501:8503 --name neo_classification neo-hazardous-classification:neo
```

## 📝 API Endpoints

- `GET /`: Welcome message
- `GET /prediction`: Make hazard predictions
  - Parameters: `absolute_magnitude`, `estimated_diameter_min`, `relative_velocity`, `miss_distance`
  - Returns: `{"prediction": "hazardous" | "not_hazardous"}`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test using Docker
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
