pipeline {
    agent any

    stages {
        stage('Install dependencies') {
            steps {
                sh 'python3 -m venv venv'
                sh 'source venv/bin/activate'
                sh 'venv/bin/python3 -m pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                sh 'source venv/bin/activate && python -m unittest test_app.py'
            }
        }

        stage('Deploy') {
            steps {
                sh 'nohup venv/bin/gunicorn --bind 0.0.0.0:5000 app:app &'
            }
        }
    }
}
