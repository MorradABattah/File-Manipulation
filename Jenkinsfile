pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                git credentialsId: 'gitcred', url: 'https://github.com/MorradABattah/File-Manipulation.git'
            }
        }
        stage('Install dependencies') {
            steps {
                script {
                    sh '''
                        python3 -m venv venv
                        . venv/bin/activate
                        python -m pip install -r requirements.txt
                    '''
                }
            }
        }
        stage('Run Tests') {
            steps {
                script {
                    sh '''
                        . venv/bin/activate
                        python -m unittest test_app.py -v
                    '''
                }
            }
            post {
                always {
                    junit 'test-reports/*.xml'
                }
            }
        }
    }
}
