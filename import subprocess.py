import os
import subprocess

# my_env = os.environ.copy()
# # my_env["PATH"] = os.pathsep.join(["/opt/myapp/", my_env["PATH"]])

# print(my_env["PATH"])
# result = subprocess.run(["myapp"], env=my_env)

cwd_subprocess = subprocess.check_output(['pwd'], text=True).strip()

print(cwd_subprocess)
