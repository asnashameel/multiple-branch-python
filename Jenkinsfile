@Library('python-library') _
pipeline {
    agent any
    environment {
        PY_IMAGE: "asnashameel/python-image:latest"
    }
    stages {
        stage('git checkout') {
            steps {
                git branch: "main", url: "https://github.com/asnashameel/multiple-branch-python.git"
            }
        }
        stage('docker build and push') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'hubtoken', passwordVariable: 'PASSWD', usernameVariable: 'USER_NAME')]) {
                    sh '''
                    docker build -t $PY_IMAGE .
                    docker login -u $USER_NAME -p $PASSWD
                    docker push $PY_IMAGE
                    
                    if docker ps -a | grep 'python-container';
                        docker stop python-container
                        docker rm python-container
                    fi
                    
                    docker run -d -p 5001:5000 --name python-container $PY_IMAGE
                    '''
                }
            }
        }
         stage('run pytest') {
            steps {
                script {
                    build()
                    echo "test done succesfully"
                }
            }
        }
        stage('deployment') {
            steps {
                sh '''
                kubectl delete deployment --all
                kubectl create deployment python-deployment --image=$PY_IMAGE --dry-run=client -o yaml >deploy.yaml
                kubectl apply -f deploy.yaml
                kubectl delete svc --all
                kubectl expose deployment python-deployment --name py-svc --port 5001 --target-port 5000 -dry-run=client -o yaml > svc.yaml
                kubectl apply -f svc.yaml
                '''
            }
        }
    }
}
