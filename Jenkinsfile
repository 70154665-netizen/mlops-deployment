pipeline {
    agent any

    environment {
        MLFLOW_TRACKING_URI = 'http://localhost:5000'
    }

    stages {
        stage('Dev Pipeline') {
            when {
                branch 'dev'
            }
            stages {
                stage('Data Ingest & Train') {
                    steps {
                        echo 'Data Ingest and Training Model...'
                        echo 'Simulating model training completed successfully.'
                    }
                }
                stage('Model Deploy & Test (Dev)') {
                    steps {
                        echo 'Deploying and Testing Model on Dev...'
                        echo 'Model Test Passed successfully.'
                    }
                }
            }
        }

        stage('Pre-prod Pipeline') {
            when {
                branch 'main'
            }
            stages {
                stage('Load & Register Challenger') {
                    steps {
                        echo 'Loading Challenger model & assigning Challenger-pre-test...'
                    }
                }
            }
        }

        stage('Prod Pipeline') {
            when {
                buildingTag()
            }
            stages {
                stage('Register Champion & Deploy') {
                    steps {
                        echo 'Assigning alias Champion and Deploying to Production...'
                    }
                }
            }
        }
    }
}
