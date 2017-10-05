from fabric.api import env, cd, run
import os

HOME = '/home/ec2-user/Rogers'

env.hosts = [os.getenv('HOST')]
env.key_filename = '~/.ssh/id_rogers'
env.warn_only = True


# Deploy to remote server
def deploy():
    with cd(HOME):
        run('git pull')
        run('pyenv shell rogers')
        print("Deploy finished!")
