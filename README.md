# python scripts for intel-pmwatch

[intel/intel-pmwatch](https://github.com/intel/intel-pmwatch): Intel® PMWatch (PersistentMemoryWatch) is a tool that monitors and reports the performance and health information metrics of the Intel® Optane™ DC Persistent Memory.

todo:
- [ ] multi-dimm watch
- [ ] support collecting data from `pcm-memory -pmm | egrep -v "NM"`


---

pmwatch里的指标（带*的代表是计算得到的）

- *bytes_read/bytes_write：具体读写的数据（ (read_64B_ops_received - write_64B_ops_received) * 64）（write_64B_ops_received * 64, media_write_ops * 256）
- *read_hit_ratio/write_hit_ratio：注意如果写>0.75或读~1，说明命中buffer。如果读or写=0.75，说明其为顺序访问特征。
- *media_read_ops/media_write_ops：media上的读写。256B为单位。通过received计算得到，注意`media_read_ops = (read_64B_ops_received - write_64B_ops_received) / 4`。
- read_64B_ops_received/write_64B_ops_received：media上的操作数（包括CPU发起的和maintenance的）。注意是以64B为单位【*注意这个值会大于cpu_write_ops，应该就是内部controller发起的，差值在idle时约12K，写密集后会增加，如单线程256B写会到~123K*】
- cpu_read_ops/cpu_write_ops：memory controller发起的读写次数。单位是64B。

所以：
- WA = media_write_ops*4/cpu_write_ops
- RA = media_read_ops*4/cpu_read_ops

这个脚本依赖PMWatch，PMWatch依赖libipmctl。lingfenghsiang/pm_util依赖的是`ipmctl show -performance`，所以开销应该是类似的。