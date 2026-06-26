pipeline {
agent any

```
environment {
    APP_DIR = "/home/ubuntu/smart-productivity-tracker"
}

stages {

    stage('Checkout') {
        steps {
            git branch: 'main',
                credentialsId: 'github-creds',
                url: 'https://github.com/Roman-ab/smart-productivity-tracker.git'
        }
    }

    stage('Backup Current Version') {
        steps {
            sh '''
            mkdir -p ~/backups

            cp docker-compose.yml ~/backups/docker-compose.yml.bak || true
            '''
        }
    }

    stage('Build') {
        steps {
            sh '''
            docker compose build
            '''
        }
    }

    stage('Deploy') {
        steps {
            sh '''
            docker compose down
            docker compose up -d
            '''
        }
    }

    stage('Health Check') {
        steps {
            sh '''
            sleep 20

            curl -f http://localhost:8000/health
            '''
        }
    }
}

post {

    success {
        echo 'Deployment successful'
    }

    failure {
        echo 'Deployment failed. Rolling back.'

        sh '''
        docker compose down

        cp ~/backups/docker-compose.yml.bak docker-compose.yml || true

        docker compose up -d
        '''
    }
}
```

}
