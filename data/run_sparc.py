import subprocess
import time

def run_sparc(directory='.', label='.', user='rbhagat8'):

    def get_process_status_output():
        command_output = subprocess.Popen(
            f'qstat -u {user}',
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
            cwd=directory
        ).communicate()[0].decode('utf-8')

        lines = command_output.split('\n')

        last_line = ''
        idx = 0

        while len(last_line) == 0:
            idx += 1
            last_line = lines[-idx]

        splt = last_line.split(' ')
        splt = [s for s in splt if len(s) > 0]

        return splt[0], splt[9]

    last_proc_name, _ = get_process_status_output()

    stdout, stderr = subprocess.Popen(
        f'qsub run_sparc.sh -F {directory} -F {label}',
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True
    ).communicate()[:2]

    proc_name, proc_status = get_process_status_output()
    while proc_name == last_proc_name or proc_status != 'C':
        proc_name, proc_status = get_process_status_output()
        print(f'{proc_name}: {proc_status}' + ' ' * 10, end='\r')
        time.sleep(2)

    return proc_name

