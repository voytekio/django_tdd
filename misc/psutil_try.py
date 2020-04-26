import psutil
import pdb

pids_to_kill = []
kill_flag = False
for one_p in psutil.process_iter():
    try:
        #print('one: {}'.format(one_p))
        if "python" in one_p.name().lower():
            #pdb.set_trace()
            if 'runserver' in one_p.cmdline() and 'python' in one_p.parent().name().lower():
                pids_to_kill.append(one_p)
    except psutil.ZombieProcess as e:
        print('ZOMBIE: {}'.format(one_p))
        pass

for one in pids_to_kill:
    print('Killing PID: {}, with cmdline: {}, parent_name: {} and connections: {}'.format(one.pid, one.cmdline(), one.parent().name(), one.connections()))
    if kill_flag:
        one.kill()
