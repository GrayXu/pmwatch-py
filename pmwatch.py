# #!/usr/bin/python3
'''
collect and calculate data from pmwatch on DIMM0
'''
import subprocess

my_cmd_string = "pmwatch 1 -td"
def execute(cmd):
    popen = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, universal_newlines=True)
    for stdout_line in iter(popen.stdout.readline, ""):
        yield stdout_line
    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)

i = 0

COLOR_TAIL = '\033[0m'
RED = "\033[91m"
GREEN = "\033[92m"
BLUE = '\033[0;36m'
BLUEE = "\033[94m"
GRAY = "\033[90m"

for path in execute(my_cmd_string.split(" ")):
    data = path.split("\t")
    if i >= 7:
        # print(data)
        ra = -1
        wa = -1
        media_read = -1
        media_write = -1
        mc_read = -1
        mc_write = -1

        # cal
        if int(data[10]) > 100 or int(data[11]) > 50:
            ra = int(data[6])*4/int(data[10])  # read amplification
            wa = int(data[7])*4/int(data[11])  # write amplification
            media_read = int(data[6])*256/1024/1024
            media_write = int(data[7])*256/1024/1024
            mc_read = int(data[10])*64/1024/1024
            mc_write = int(data[11])*64/1024/1024

        for i in range(1):
            print(int(data[i])%10000, end=",")
        for i in range(4, 6):
            print(data[i], end=",")

        if ra == -1:
            print(str(GRAY+"RA="+"%.2f"+COLOR_TAIL) % ra,                         end=",")
        else:
            print(RED+"RA="+COLOR_TAIL+"%.2f" % ra,                               end=",")

        if wa == -1:
            print(str(GRAY+"WA="+"%.2f"+COLOR_TAIL) % wa,                         end=",")
        else:
            print(RED+"WA="+COLOR_TAIL+"%.2f" % wa,                               end=",")


        print(GREEN+"me_R/W="+COLOR_TAIL+"%.2f" % (media_read/media_write),       end=",")
        print(GREEN+"mc_R/W="+COLOR_TAIL+"%.2f" % (mc_read/mc_write),             end=",")
        
        if media_read == -1:
            print(str(GRAY+"me_R="+"%.2f"+COLOR_TAIL) % media_read,               end=",")
        else:
            print(BLUE+"me_R="+COLOR_TAIL+"%.2f" % media_read,                    end=",")
        
        if media_write == -1:
            print(str(GRAY+"me_W="+"%.2f"+COLOR_TAIL) % media_write,              end=",")
        else:
            print(BLUE+"me_W="+COLOR_TAIL+"%.2f" % media_write,                   end=",")

        if mc_read == -1:
            print(str(GRAY+"mc_R="+"%.2f"+COLOR_TAIL) % mc_read,                  end=",")
        else:
            print(BLUE+"mc_R="+COLOR_TAIL+"%.2f" % mc_read,                       end=",")

        if mc_write == -1:
            print(str(GRAY+"mc_W="+"%.2f"+COLOR_TAIL) % mc_write,                 end=",")
        else:
            print(BLUE+"mc_W="+COLOR_TAIL+"%.2f" % mc_write,                      end=",")
            

        print("\n")
    i += 1
