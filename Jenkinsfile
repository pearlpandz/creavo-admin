pipeline {
    agent any

    options {
        timestamps()
        disableConcurrentBuilds()
    }

    parameters {
        choice(
            name: 'ENV',
            choices: ['dev', 'prod'],
            description: 'Select deployment environment'
        )
    }

    environment {
        PROJECT_NAME = "creavo-frontend"
        NODE_VERSION = "18"
    }

    stages {

        stage("Resolve Environment") {
            steps {
                script {
                    env.DEPLOY_ENV = "${ENV}"
                    env.DEPLOY_BASE = "/var/www/${env.DEPLOY_ENV}/frontend/${PROJECT_NAME}"
                    env.RELEASE_DIR = "${env.DEPLOY_BASE}/releases/${BUILD_TIMESTAMP}"
                    env.CURRENT_DIR = "${env.DEPLOY_BASE}/current"

                    env.ENV_FILE = env.DEPLOY_ENV == "prod"
                        ? "/etc/creavo/dev/django-admin.env"
                        : "/etc/creavo/prod/django-admin.env"

                    echo """
                    ✅ React Environment Resolved
                    Branch      : ${env.BRANCH_NAME}
                    Env         : ${env.DEPLOY_ENV}
                    Deploy Dir  : ${env.DEPLOY_BASE}
                    Env File    : ${env.ENV_FILE}
                    """
                }
            }
        }

        stage("Checkout") {
            steps {
                checkout scm
            }
        }

        stage("Validate Environment Variables") {
            steps {
                sh """
                if [ ! -f ${ENV_FILE} ]; then
                  echo "❌ Env file missing: ${ENV_FILE}"
                  exit 1
                fi

                REQUIRED_VARS=(
                  REACT_APP_API_BASE_URL
                  REACT_APP_MEDIA_URL
                )

                for VAR in "\${REQUIRED_VARS[@]}"; do
                  if ! grep -q "^$VAR=" ${ENV_FILE}; then
                    echo "❌ Missing env variable: $VAR"
                    exit 1
                  fi
                done

                echo "✅ All required env vars present"
                """
            }
        }

        stage("Prepare Release") {
            steps {
                sh """
                mkdir -p ${RELEASE_DIR}
                rsync -a --exclude=.git --exclude=node_modules ./ ${RELEASE_DIR}/
                cp ${ENV_FILE} ${RELEASE_DIR}/.env
                """
            }
        }

        stage("Install Dependencies") {
            steps {
                sh """
                cd ${RELEASE_DIR}
                npm ci
                """
            }
        }

        stage("Build React App") {
            steps {
                sh """
                cd ${RELEASE_DIR}
                npm run build
                """
            }
        }

        stage("Activate Release") {
            steps {
                sh """
                ln -sfn ${RELEASE_DIR}/build ${CURRENT_DIR}
                """
            }
        }

        stage("Reload NGINX") {
            steps {
                sh """
                sudo systemctl reload nginx
                """
            }
        }
    }

    post {
        success {
            echo "✅ React app deployed successfully to ${ENV}"
        }
        failure {
            echo "❌ React deployment failed on ${ENV}"
        }
    }
}
