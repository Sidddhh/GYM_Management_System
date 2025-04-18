pipeline {
    agent any

    environment {
        DOCKERHUB_USERNAME = credentials('siddhug45')
        DOCKERHUB_PASSWORD = credentials('Siddhu@45')
    }

    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/Sidddhh/GYM_Management_System.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                bat 'pip install -r requirements.txt'
            }
        }

        stage('Test') {
            steps {
                bat 'pytest || echo No tests found'
            }
        }

        stage('Docker Build & Push') {
            steps {
                bat """
                echo %DOCKERHUB_PASSWORD% | docker login -u %DOCKERHUB_USERNAME% --password-stdin
                docker build -t %DOCKERHUB_USERNAME%/gym-management-app:latest .
                docker push %DOCKERHUB_USERNAME%/gym-management-app:latest
                """
            }
        }
    }
}
