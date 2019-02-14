# Lempel-Ziv #
In order to run a test of the encoder and decoder:

1 - Place your target file in the "originals" folder

2 - Open a command console and navigate to the directory where lz77_test.py is

3 - Run the command python lz77_test.py [filename.extension] [window size in bytes] [buffer size in bytes]

Note: The compressor only supports window and buffer sizes up to 65536 bytes.

The file in originals will be compressed into the folder binaries as a filename.bin file.

The decompressed file will be located in the folder decompressed as filenameDecomp.extension


You can modify the nature of the tests in lz77_test.py. There are comments which point to what does what.
