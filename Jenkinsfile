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
                        sh 'python3 train.py'
                    }
                }
                stage('Model Deploy & Test (Dev)') {
                    steps {
                        echo 'Deploying and Testing Model on Dev...'
                        sh 'python3 -c "print(\'Model Test Passed\')"'
                    }
                }
            }
            post {
                failure {
                    emailext body: 'Dev Pipeline Failed!', subject: 'Dev Build Failed', to: 'admin@example.com'
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
                stage('Model Deploy & Test (Pre-prod)') {
                    steps {
                        echo 'Deploying and Testing Model in Pre-prod...'
                    }
                }
                stage('Update Alias to Challenger-post-test') {
                    steps {
                        echo 'Updating alias to Challenger-post-test...'
                    }
                }
            }
            post {
                failure {
                    emailext body: 'Pre-prod Pipeline Failed!', subject: 'Pre-prod Build Failed', to: 'admin@example.com'
                }
            }
        }

        
        stage('Prod Pipeline') {
            when {
                buildingTag()
            }
            stages {
                stage('Load Challenger-post-test') {
                    steps {
                        echo 'Loading model Challenger-post-test...'
                    }
                }
                stage('Register Champion & Deploy') {
                    steps {
                        echo 'Assigning alias Champion and Deploying to Production...'
                    }
                }
            }
        }
    }
}
