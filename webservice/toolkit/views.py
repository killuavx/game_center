# -*- encoding=utf-8 -*-
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect

GC_CMD_RESTART_EXE = '/home/www-data/scripts/gc-restart.sh'


def sys_user_belong(group_name):
    def in_operator(user):
        return user.groups.filter(name=group_name).exists()
    return in_operator


@user_passes_test(sys_user_belong(group_name='operator'), login_url='/admin/')
def sys_restart(request, *args, **kwargs):
    import sh
    restart = sh.Command(GC_CMD_RESTART_EXE)
    try:
        restart()
        messages.info(request, 'Restart System Successfully!')
    except:
        messages.info(request, 'Restart System Failure!')
    return redirect('admin:index')
