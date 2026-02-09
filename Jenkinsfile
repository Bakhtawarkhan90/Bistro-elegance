pipeline {
    agent any
    environment {
        SONAR_HOME = tool "Sonar"
        GITHUB_USERNAME = 'Bakhtawarkhan90'   // Replace with your GitHub username
    }
    stages {
        stage("Workspace Clean-up") {
            steps {
                script {
                    cleanWs()
                }
            }
        }
        stage("Cloning Code") {
            steps {
                git url: "https://github.com/Bakhtawarkhan90/Bistro-elegance.git", branch: "main"
            }
        }
        stage("Sonarqube Code Analysis") {
            steps {
                withSonarQubeEnv("Sonar") {
                    sh "$SONAR_HOME/bin/sonar-scanner -Dsonar.projectName=Bistro -Dsonar.projectKey=Bistro -X"
                }
            }
        }
        stage("Download SonarQube Report") {
            steps {
                script {
                    sh """
                    curl -u admin:admin "13.126.6.42:9000/api/measures/component?component=Bistro&metricKeys=bugs,vulnerabilities,code_smells,coverage,duplicated_lines_density" -o sonar-report.json
                    """
                }
            }
        }
        stage("Docker Image Building") {
            steps {
                sh "docker build . -t bistro:latest"
            }
        }
        stage('Trivy Image Scanning') {
            steps {
                echo "Trivy Image Scanning"
                retry(3) {
                    sh 'trivy image bistro:latest || sleep 60'
                }
            }
        }
        stage("Push Docker-Hub") {
            steps {
                withCredentials([usernamePassword(credentialsId: "dockerHub", passwordVariable: "dockerHubPass", usernameVariable: "dockerHubUser")]) {
                    sh "echo \$dockerHubPass | docker login -u \$dockerHubUser --password-stdin"
                    sh "docker tag bistro:latest ${env.dockerHubUser}/bidtro:latest"
                    sh "docker push ${env.dockerHubUser}/bistro:latest"
                }
            }
        }
        stage("Run Docker Container ") {
            steps {
                sh " docker compose down & docker compose up -d --build"
            }
        }
    }
    post {
        success {
            mail to: 'royalbakhtawar@gmail.com',
                subject: "Pipeline Success: ${currentBuild.fullDisplayName}",
                body: "The Pipeline '${env.JOB_NAME}' has successfully completed.\n" +
                      "Check it here: ${env.BUILD_URL}"
        }
        failure {
            mail to: 'royalbakhtawar@gmail.com',
                subject: "Pipeline Failed: ${currentBuild.fullDisplayName}",
                body: "The Pipeline '${env.JOB_NAME}' has failed.\n" +
                      "Check it here: ${env.BUILD_URL}"
        }
    }
}
