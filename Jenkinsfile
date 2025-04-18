pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-creds')
    }

    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/Sidddhh/GYM_Management_System.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                // Install requirements locally for testing — use --user for permission issues
                bat 'pip install --user -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                // Run pytest — now that you have test_dummy.py, this will pick it up
                bat 'pytest'
            }
        }

        stage('Docker Build & Push') {
            steps {
                bat """
                echo %DOCKERHUB_CREDENTIALS_PSW% | docker login -u %DOCKERHUB_CREDENTIALS_USR% --password-stdin
                docker build -t %DOCKERHUB_CREDENTIALS_USR%/gym-management-app:latest .
                docker push %DOCKERHUB_CREDENTIALS_USR%/gym-management-app:latest
                """
            }
        }
    }

    post {
        success {
            echo '✅ Pipeline completed successfully!'
        }
        failure {
            echo '❌ Pipeline failed. Check logs above.'
        }
    }
}
