pipeline {
    agent any
    stages {
        stage('Get Code') {
            steps { checkout scm }
        }
        stage('Check Python Code') {
            steps {
                sh 'pip3 install -r requirements.txt'
                sh 'python3 -m py_compile app.py'
            }
        }
        stage('Build Docker Image') {
            steps {
                sh 'docker build -t YOUR_DOCKERHUB_USERNAME/student-attendance:latest .'
            }
        }
        stage('Push Image') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-login',
                    usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh 'echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin'
                    sh 'docker push YOUR_DOCKERHUB_USERNAME/student-attendance:latest'
                    sh 'docker logout'
                }
            }
        }
    }
}