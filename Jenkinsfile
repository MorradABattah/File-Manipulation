pipeline {
    agent any

    stages {
        stage('Install dependencies') {
            steps {
                script {
                    sh '''
                        python3 -m venv venv
                        source venv/bin/activate
                        venv/bin/python3 -m pip install -r requirements.txt
                    '''
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    sh '''
                        source venv/bin/activate 
                        python -m unittest test_app.py
                    '''
                }
            }
            post {
                always {
                    junit '**/test-results.xml'
                }
            }
        }

        stage('Deploy') {
            steps {
                sh 'nohup venv/bin/gunicorn --bind 0.0.0.0:5000 app:app &'
            }
        }
    }
    
    post {
        always {
            archiveArtifacts artifacts: 'app.log', fingerprint: true
            cleanWs()
        }
    }
}
