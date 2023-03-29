import subprocess
import time


def run_sparc(directory=".", label="sparc-calc", user="rbhagat8"):
    """Runs sparc using a subprocess and the parameters provided

    Args:
        directory (str, optional): The directory to run sparc in. Defaults to ".".
        label (str, optional): The label to use for the input and output files. Defaults to "sparc-calc".
        user (str, optional): The user to run it under (and send emails to). Defaults to "rbhagat8".
    """
    def get_process_status_output():
        command_output = (
            subprocess.Popen(
                f"squeue -u {user}",
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True,
                cwd=directory,
            )
            .communicate()[0]
            .decode("utf-8")
        )

        lines = command_output.split("\n")

        for line in lines:
            if len(line) == 0:
                continue
            splt = line.split(" ")
            splt = [s for s in splt if len(s) > 0]

            names = "JOBID PARTITION NAME USER ST TIME NODES NODELIST(REASON)".lower().split(" ")

            props = {k:v for k,v in zip(names, splt)}
        
            if "RunDevSparc".startswith(props["name"]):
                return props["jobid"], props["st"], props["name"]
            
        return "JOBID", "ST", "NAME"

    stdout, stderr = subprocess.Popen(
        f"sbatch --export=directory={directory},label={label} RunDevSparc.sbatch",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
    ).communicate()[:2]

    job_id, _, _ = get_process_status_output()

    while job_id == "JOBID":
        job_id, proc_status, name = get_process_status_output()
        print(f"{name} --> {job_id}: {proc_status}" + " " * 10, end="\r")
        time.sleep(1)

    while job_id != "JOBID":
        job_id, proc_status, name = get_process_status_output()
        print(f"{name} --> {job_id}: {proc_status}" + " " * 10, end="\r")
        time.sleep(2)

    return job_id


if __name__ == "__main__":
    print(run_sparc())
