# A wrapper for intel-pmwatch with colorization

```bash
$ python3 pmwatch.py 0 # To watch DIMM0
```

[intel/intel-pmwatch](https://github.com/intel/intel-pmwatch): Intel® PMWatch (PersistentMemoryWatch) is a tool that monitors and reports the performance and health information metrics of the Intel® Optane™ DC Persistent Memory.

TODO:
- [x] colorize
- [x] multi-dimm watch
- [ ] collecting data from `pcm-memory`
- [ ] loads watch


---

The metrics in pmwatch (indicated by *) are as follows:

- *bytes_read/bytes_write: The actual amount of data read and written, calculated as (read_64B_ops_received - write_64B_ops_received) * 64 for reads and write_64B_ops_received * 64 or media_write_ops * 256 for writes.
- *read_hit_ratio/write_hit_ratio: If write > 0.75 or read is close to 1, it indicates a buffer hit. If read or write = 0.75, it indicates a sequential access pattern.
- *media_read_ops/media_write_ops: The number of reads and writes on the media, measured in units of 256B. Calculated using the received values, where `media_read_ops = (read_64B_ops_received - write_64B_ops_received) / 4`.
- read_64B_ops_received/write_64B_ops_received: The number of operations on the media (including CPU-initiated and maintenance operations), measured in units of 64B. *Note that this value may be greater than cpu_write_ops, as it includes operations initiated by the internal controller. The difference is around 12K during idle and increases during write-intensive operations, such as a single-threaded 256B write reaching ~123K.*
- cpu_read_ops/cpu_write_ops: The number of read and write operations initiated by the memory controller, measured in units of 64B.

Therefore:  
WA = media_write_ops * 4 / cpu_write_ops  
RA = media_read_ops * 4 / cpu_read_ops  
This script depends on PMWatch, which in turn depends on libipmctl. [lingfenghsiang/pm_util](https://github.com/lingfenghsiang/pm_util) depends on `ipmctl show -performance`, so the overhead should be similar.