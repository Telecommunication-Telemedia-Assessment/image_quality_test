first run

```
./prepare.sh
```
(here requirements for VMAF are needed, and git)

afterwards, run
```
./create_encode_commands.py src_cropped
```

this will create the file `encode_commands.list`
that can be executed via:

```
cat encode_commands.list | xargs -P10
```
(here ffmpeg is required)

after this you can extract the filesizes with `./get_filesize.sh`
and calculate objective metrics with `./create_commands_vmaf.py`,
this script will create a list `vmaf_cmds.list` that can be run similar to encode_commands.list via
```
cat vmaf_cmds.list | xargs -P10
```

finally the `./select_representations.py` script selects based on vmaf the used images for the test.

To calculate SI and VCA you need the corresponding tools locally installed.
For VCA you need to add a specific output of json to the tool.
