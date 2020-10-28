import os
import json
import dmenu
from subprocess import Popen, PIPE

import functools
 
def_file = 'hist.json'
HISTORY = os.path.join(os.environ['HOME'], '.config/portmapper/')


def show(iters, defs=None, prompt='Choose: '):
    r = dmenu.show(iters, prompt=prompt)
    if r:
        return r
    else:
        raise Exception


def load_hist():
    try:
        with open(os.path.join(HISTORY , def_file), 'r') as f:
            data = json.load(f)
    except:
        data = []
        
    return data

def update_hist(hist, item):
    st = json.dumps(item)#, indent=4)
    hist_strs = [json.dumps(i) for i in hist]
    if st not in hist_strs:
        hist.append(item)
        with open(os.path.join(HISTORY, def_file), 'w') as f:
            json.dump(hist, f, indent=4)    

def unique(func):
    @functools.wraps(func)
    def wrapper_uni(*args, **kwargs):
        res = func(*args, **kwargs)
        seen = set()
        ordered_uni_res = []
        for i in res:
            if i not in seen:
                seen.add(i)
                ordered_uni_res.append(i)
        return ordered_uni_res
        
    return wrapper_uni

@unique
def get_urls(hist):
    return [i['url'] for i in hist]

@unique
def get_ports(hist, local=False):
    if local:
        return [str(v['local_port']) for v in hist]
    else:   
        return [str(v['host_port']) for v in hist]

@unique
def get_users(hist):
    return [v['user'] for v in hist]

def create_output(out, err):
    msg = {'level':'normal', 'txt':'Successful port forwarding', 'timer':'2000'}
    if err:
        msg['level']='critical'
        msg['txt'] = 'Error \n' + err.decode('utf-8')
        msg['timer']= '5000'
    return msg

if __name__ == '__main__':
    hist = load_hist()
    
    def_users = get_users(hist)
    def_urls = get_urls(hist)
    def_local_ports = get_ports(hist, local=True)
    def_host_ports = get_ports(hist, local=False)
    
    user = show(def_users, prompt='Select USER: ')
    url = show(def_urls, prompt='Select URL: ')
    host_port = show(def_host_ports, prompt='Select HOST port: ')
    local_port = show(def_local_ports, prompt='Select LOCAL port: ')
    item =  {'url':url, 'user':user, 'host_port':host_port, 'local_port':local_port}
    
    update_hist(hist, item)
    
    process = Popen(['ssh', '-N', '-L', f'{local_port}:127.0.0.1:{host_port}', f'{user}@{url}', '&'], stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()

    msg = create_output(stdout, stderr)

    process = Popen(['notify-send', msg['txt'], '-u', msg['level'], '-t', msg['timer']], stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
