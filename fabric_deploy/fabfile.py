import os
from fabric.api import cd, env, task, require, sudo, prefix
from fabric.contrib.files import exists, upload_template


VIRTUALENV_DIR = 'env'
CODE_DIR = 'app'
PACKAGES = (
    'python-dev',
    'python-virtualenv',
    'supervisor',
)
LOG_DIR = 'logs'


@task
def demo():
    env.server_name = 'demo.storyweb.grano.cc'
    env.deploy_user = 'fl'
    env.deploy_dir = '/var/www/%s/' % env.server_name
    env.repo_dir = os.path.join(env.deploy_dir, CODE_DIR)
    env.branch = 'master'
    env.nginx_bind = '127.0.0.1:80'
    env.proxy_host = '127.0.0.1'
    env.proxy_port = 11020
    env.hosts = ['norton.pudo.org']


@task
def provision():
    require('deploy_user', 'deploy_dir', provided_by=[demo])

    commands = (
        'apt-get install -y %s --no-upgrade' % ' '.join(PACKAGES),
        'apt-get build-dep -y lxml --no-upgrade',
        'mkdir -p %s' % env.deploy_dir,
        'chown -R %s:%s %s' % (env.deploy_user, env.deploy_user, env.deploy_dir),
    )
    sudo('; '.join(commands))


@task
def deploy():
    require('deploy_user', 'deploy_dir', 'branch',
            provided_by=[demo])

    ve_dir = os.path.join(env.deploy_dir, VIRTUALENV_DIR)

    if not exists(ve_dir):
        sudo('virtualenv -p python2.7 %s' % ve_dir, user=env.deploy_user)

    if not exists(env.repo_dir):
        with cd(env.deploy_dir):
            sudo('git clone -b %s https://github.com/granoproject/storyweb.git %s'
                 % (env.branch, env.repo_dir), user=env.deploy_user)
    else:
        with cd(env.repo_dir):
            sudo('git checkout -B %s' % env.branch, user=env.deploy_user)
            sudo('git pull origin %s' % env.branch, user=env.deploy_user)

    with cd(env.repo_dir), prefix('. ../%s/bin/activate' % VIRTUALENV_DIR):
        sudo('pip install -e ./', user=env.deploy_user)
        sudo('pip install -r requirements.txt', user=env.deploy_user)
        sudo('bower install', user=env.deploy_user)

    # render and upload templates
    upload_template(os.path.join(os.path.dirname(__file__), 'nginx.template'),
                    '/etc/nginx/sites-enabled/%s' % env.server_name,
                    get_nginx_template_context(), use_sudo=True, backup=False)
    upload_template(os.path.join(os.path.dirname(__file__), 'supervisor.template'),
                    '/etc/supervisor/conf.d/%s.conf' % env.server_name,
                    get_supervisor_template_context(), use_sudo=True, backup=False)
    # make sure logging dir exists and update processes
    log_dir = os.path.join(env.deploy_dir, LOG_DIR)
    sudo('mkdir -p %s' % log_dir, user=env.deploy_user)
    sudo('supervisorctl update')
    sudo('/etc/init.d/nginx reload')


def get_nginx_template_context():
    static_dir = '%s/storyweb/static/' % env.repo_dir
    return {
        'server-name': env.server_name,
        'server-port': env.nginx_bind,
        'static-path': os.path.join(env.deploy_dir, static_dir),
        'log': os.path.join(env.deploy_dir, LOG_DIR, 'nginx.log'),
        'err-log': os.path.join(env.deploy_dir, LOG_DIR, 'nginx.err'),
        'proxy-host': env.proxy_host,
        'proxy-port': env.proxy_port
    }


def get_supervisor_template_context():
    return {
        'server-name': env.server_name,
        'user': env.deploy_user,
        'deploy-dir': env.deploy_dir,
        'project-dir': os.path.join(env.deploy_dir, CODE_DIR),
        've-dir': os.path.join(env.deploy_dir, VIRTUALENV_DIR),
        'gunicorn-log': os.path.join(env.deploy_dir, LOG_DIR, 'gunicorn.log'),
        'gunicorn-err-log': os.path.join(env.deploy_dir, LOG_DIR, 'gunicorn.err'),
        'celery-log': os.path.join(env.deploy_dir, LOG_DIR, 'celery.log'),
        'celery-err-log': os.path.join(env.deploy_dir, LOG_DIR, 'celery.err'),
        'host': env.proxy_host,
        'port': env.proxy_port
    }
