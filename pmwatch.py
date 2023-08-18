# #!/usr/bin/python3
'''
collect and calculate data from pmwatch
'''
import subprocess
import sys

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

'''
the first two are epoch and timestamp
each DIMM has 10 data columns
example outpus in `pmwatch_example_output`
'''
DATA_LEN = 10

COLOR_TAIL = '\033[0m'
RED = "\033[91m"
GREEN = "\033[92m"
BLUE = '\033[0;36m'
BLUEE = "\033[94m"
GRAY = "\033[90m"


'''
handle data with len==10
'''
def print_per_dimm(data):
    ra = -1
    wa = -1
    media_read = -1
    media_write = -1
    MC_Read = -1
    MC_Write = -1

    # cal
    for i in range(2, 4):
        print(data[i], end=",")
    if int(data[8]) > 100 or int(data[9]) > 50:
        ra = int(data[4])*4/int(data[8])  # read amplification
        wa = int(data[5])*4/int(data[9])  # write amplification
        media_read = int(data[4])*256/1024/1024
        media_write = int(data[5])*256/1024/1024
        MC_Read = int(data[8])*64/1024/1024
        MC_Write = int(data[9])*64/1024/1024

    # output
    if ra == -1:
        print(str(GRAY+"RA="+"%.2f"+COLOR_TAIL) % ra,                         end=",")
    else:
        print(RED+"RA="+COLOR_TAIL+"%.2f" % ra,                               end=",")

    if wa == -1:
        print(str(GRAY+"WA="+"%.2f"+COLOR_TAIL) % wa,                         end=",")
    else:
        print(RED+"WA="+COLOR_TAIL+"%.2f" % wa,                               end=",")


    print(GREEN+"Me_R/W="+COLOR_TAIL+"%.2f" % (media_read/media_write),       end=",")
    print(GREEN+"MC_R/W="+COLOR_TAIL+"%.2f" % (MC_Read/MC_Write),             end=",")
    
    if media_read == -1:
        print(str(GRAY+"Me_R="+"%.2f"+COLOR_TAIL) % media_read,               end=",")
    else:
        print(BLUE+"Me_R="+COLOR_TAIL+"%.2f" % media_read,                    end=",")
    
    if media_write == -1:
        print(str(GRAY+"Me_W="+"%.2f"+COLOR_TAIL) % media_write,              end=",")
    else:
        print(BLUE+"Me_W="+COLOR_TAIL+"%.2f" % media_write,                   end=",")

    if MC_Read == -1:
        print(str(GRAY+"MC_R="+"%.2f"+COLOR_TAIL) % MC_Read,                  end=",")
    else:
        print(BLUE+"MC_R="+COLOR_TAIL+"%.2f" % MC_Read,                       end=",")

    if MC_Write == -1:
        print(str(GRAY+"MC_W="+"%.2f"+COLOR_TAIL) % MC_Write,                 end=",")
    else:
        print(BLUE+"MC_W="+COLOR_TAIL+"%.2f" % MC_Write,                      end=",")
    print("")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("WRONG USAGE!!\npython3 pmwatch.py $(DIMM_IDs) (e.g. `$python3 pmwatch.py 0`)")
        exit(0)

    dimm_id_list = []
    for i in range(1, len(sys.argv)):
        dimm_id_list.append(int(sys.argv[i]))

    _ = 0
    for path in execute(my_cmd_string.split(" ")):
        data = path.split("\t")
        if _ >= 7:  # real output!
            # print(data)

            # timestamp header
            for i in range(1):
                print(int(data[i])%10000, end=",")
            if len(sys.argv) >= 2:
                print("")
            
            data = data[2:]  # cut headers
            for dimm_id in dimm_id_list:
                print_per_dimm(data[dimm_id*DATA_LEN:(dimm_id+1)*DATA_LEN])

        _ += 1
