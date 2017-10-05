from fabric.api import env, cd, run
import os

HOME = '/home/ec2-user/Rogers'

env.hosts = [os.getenv('HOST')]
env.key_filename = '~/.ssh/id_rogers'
env.warn_only = True


# Pull from remote repository
def deploy():
    with cd(HOME):
        run('git pull')
        run('source /home/ec2-user/venv/bin/activate')
        run('pip install -r requirements.txt')
