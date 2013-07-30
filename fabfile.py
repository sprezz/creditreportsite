# -*- coding:utf-8 -*-
from fabric.api import run, env, sudo, cd
from os import path, environ


TARGET_DEFAULT = 'default'

env.hosts = ['freescore560.com']
#env.user = 'django'
#env.key_filename = path.join(environ['HOME'], '.ssh/tracker.pem')

env.roledefs = {
    TARGET_DEFAULT: [],
}

INTERPRETER_DEFAULT = '/home/django/.virtualenvs/creditreportsite/bin/python'
SUPERVISORCTL = '/home/django/.virtualenvs/fbcloaker/bin/supervisorctl'

env.settings = {
    TARGET_DEFAULT: {
        'sources_folder': '/home/django/projects/creditreportsite',
        'instance': 'django-creditreportsite',
        'interpreter': INTERPRETER_DEFAULT,
        'supervisorctl': SUPERVISORCTL,
        'celery_tasks': '',
        'touch_to_reload': ['/etc/uwsgi/available/freescore560.ini', '/etc/uwsgi/available/newsreportlive.ini']
    },
}


def get_settings(role):
    return env.settings[role]


def deploy():
    for role in env.roles:
        settings = get_settings(role)
        with cd(settings['sources_folder']):
            sudo('git pull', user='django')
            sudo('%(interpreter)s manage.py syncdb --noinput' % settings, user='django')
            sudo('%(interpreter)s manage.py migrate --noinput' % settings, user='django')
            sudo('%(interpreter)s manage.py collectstatic --noinput' % settings, user='django')

            for instance in settings['touch_to_reload']:
                sudo('touch %s' % instance)

            if settings.get('celery_tasks'):
                sudo('%(supervisorctl)s restart %(celery_tasks)s' % settings)
