# #!/usr/bin/python3
'''
collect and calculate data from pmwatch on DIMM0
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
格式见pmwatch_example_output
前两个是epoch和timestamp
每个DIMM有10个数据
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
    mc_read = -1
    mc_write = -1

    # cal
    for i in range(2, 4):
        print(data[i], end=",")
    if int(data[8]) > 100 or int(data[9]) > 50:
        ra = int(data[4])*4/int(data[8])  # read amplification
        wa = int(data[5])*4/int(data[9])  # write amplification
        media_read = int(data[4])*256/1024/1024
        media_write = int(data[5])*256/1024/1024
        mc_read = int(data[8])*64/1024/1024
        mc_write = int(data[9])*64/1024/1024

    # output
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
    print("")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("WRONG USAGE!! python3 pmwatch.py $(DIMM_IDs to be watched) (e.g. `$python3 pmwatch.py 0`)")
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
