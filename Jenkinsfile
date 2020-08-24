#!groovy

pipeline {
    options {
        timestamps()
        disableConcurrentBuilds()
    }

    agent none

    stages {
        stage('Trigger Docker Build') {
            when {
                branch 'master'
                beforeAgent true
            }
            agent none
            steps {
                build (
                    job: '../docker-hamlet/master'
                )
            }
        }
    }
}
