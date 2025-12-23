pipeline {
    agent any

    options {
        timestamps()
        disableConcurrentBuilds()
    }

    parameters {
        choice(
            name: 'ENV',
            choices: ['dev', 'staging', 'prod'],
            description: 'Select deployment environment'
        )
        string(
            name: 'BRANCH',
            defaultValue: 'master',
            description: 'Select branch to build'
        )
    }

    environment {
        PROJECT_NAME = "creavo-admin"
        PYTHON       = "/usr/bin/python3"
    }

    stages {

        stage("Resolve Environment") {
            steps {
                script {
                    env.DEPLOY_ENV = params.ENV

                    env.DEPLOY_BASE = "/var/www/${env.DEPLOY_ENV}/backend/${PROJECT_NAME}"
                    env.RELEASE_DIR = "${env.DEPLOY_BASE}/releases/${BUILD_TIMESTAMP}"
                    env.CURRENT_DIR = "${env.DEPLOY_BASE}/current"

                    env.VENV_PATH = "${env.RELEASE_DIR}/venv"
                    env.DJANGO_SETTINGS_MODULE = "myapp.settings"

                    env.ENV_FILE = "/etc/creavo/${env.DEPLOY_ENV}/django-admin.env"

                    echo """
                    ✅ Environment resolved
                    Branch     : ${params.BRANCH}
                    Env        : ${env.DEPLOY_ENV}
                    Deploy Dir : ${env.DEPLOY_BASE}
                    Settings   : ${env.DJANGO_SETTINGS_MODULE}
                    Env File   : ${env.ENV_FILE}
                    Service    : ${env.GUNICORN_SERVICE}
                    """
                }
            }
        }

        stage("Checkout") {
            steps {
                checkout([$class: 'GitSCM', branches: [[name: 'refs/heads/${params.BRANCH}']], doGenerateSubmoduleConfigurations: false, extensions: [], submoduleCfg: [], userRemoteConfigs: [[url: 'https://github.com/creavo/creavo-admin.git']]])
            }
        }

        stage("Prepare Release") {
            steps {
                sh """
                mkdir -p ${RELEASE_DIR}
                rsync -a --exclude=.git --exclude=venv ./ ${RELEASE_DIR}/
                """
            }
        }

        stage("Virtualenv & Dependencies") {
            steps {
                sh """
                ${PYTHON} -m venv ${VENV_PATH}
                ${VENV_PATH}/bin/pip install --upgrade pip
                ${VENV_PATH}/bin/pip install -r ${RELEASE_DIR}/requirements.txt
                """
            }
        }

        stage("Django Checks") {
            steps {
                sh """
                cd ${RELEASE_DIR}
                ${VENV_PATH}/bin/python manage.py check
                """
            }
        }

        stage("Migrations") {
            steps {
                sh """
                cd ${RELEASE_DIR}
                ${VENV_PATH}/bin/python manage.py migrate --noinput
                """
            }
        }

        stage("Create Superuser (Safe)") {
            when {
                branch "master"
            }
            steps {
                withCredentials([
                    string(credentialsId: 'django_admin_user',  variable: 'ADMIN_USER'),
                    string(credentialsId: 'django_admin_pass',  variable: 'ADMIN_PASS'),
                    string(credentialsId: 'django_admin_email', variable: 'ADMIN_EMAIL')
                ]) {
                    sh """
                    cd ${RELEASE_DIR}
                    ${VENV_PATH}/bin/python manage.py shell << EOF
from django.contrib.auth import get_user_model
User = get_user_model()

if not User.objects.filter(username="${ADMIN_USER}").exists():
    User.objects.create_superuser(
        "${ADMIN_USER}",
        "${ADMIN_EMAIL}",
        "${ADMIN_PASS}"
    )
    print("✅ Superuser created")
else:
    print("ℹ️ Superuser already exists")
EOF
                    """
                }
            }
        }

        stage("Collect Static") {
            steps {
                sh """
                cd ${RELEASE_DIR}
                ${VENV_PATH}/bin/python manage.py collectstatic --noinput
                """
            }
        }

        stage("Activate Release") {
            steps {
                sh """
                ln -sfn ${RELEASE_DIR} ${CURRENT_DIR}
                """
            }
        }

        stage("Restart Service") {
            steps {
                sh """
                sudo systemctl restart ${GUNICORN_SERVICE}
                """
            }
        }
    }

    post {
        success {
            echo "✅ ${PROJECT_NAME} deployed successfully to ${DEPLOY_ENV}"
        }
        failure {
            echo "❌ Deployment failed on ${DEPLOY_ENV}"
        }
    }
}
