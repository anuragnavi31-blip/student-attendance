# Student Attendance Management System

A small beginner-level Python project. It can add students, mark them Present or Absent, and show an attendance report.

## Tools
Python, Flask, SQLite, GitHub, Jenkins, Docker, Docker Hub and Kubernetes.

## Run locally
Install Python, then run:

```bash
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000.

## Push code to GitHub
Create an empty repository, then run these commands. Replace the URL with your own repository URL.

```bash
git init
git add .
git commit -m "My attendance project"
git branch -M main
git remote add origin YOUR_GITHUB_REPOSITORY_URL
git push -u origin main
```

## Docker
```bash
docker build -t student-attendance .
docker run -p 5000:5000 student-attendance
```

## Jenkins and Docker Hub
1. Set up Jenkins with Git, Python and Docker available.
2. Add Docker Hub username and access token as Jenkins credentials with ID `dockerhub-login`.
3. Replace `YOUR_DOCKERHUB_USERNAME` in `Jenkinsfile`.
4. Create a Jenkins Pipeline job linked to the GitHub repository.
5. Run the pipeline. It downloads the code, checks Python syntax, builds the image and pushes it to Docker Hub.

## Kubernetes
Replace `YOUR_DOCKERHUB_USERNAME` in `k8s-deployment.yaml`, then run:

```bash
kubectl apply -f k8s-deployment.yaml
kubectl get pods
kubectl get services
```

Open your cluster's address on port 30080. The exact address depends on your Kubernetes setup.

## Pipeline flow
Code → GitHub → Jenkins → Check code → Docker image → Docker Hub → Kubernetes

This is a learning project and is not intended for real student records.
