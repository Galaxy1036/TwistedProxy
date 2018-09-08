var readPtr = Module.findExportByName('libc.so', 'read');

var read = new NativeFunction(readPtr, 'int', ['int', 'pointer', 'int']);


Interceptor.replace(readPtr, 
	new NativeCallback(function(fd, buf, count) {
		// Since the only time the game read 32 bytes on a file
		// is when he generate sk from /dev/urandom we don't have to deal with 
		// file descriptor to be sure 32 bytes are read on /dev/urandom

		if (count == 32) {
			// 32 times 0x00 seems to trigger the game and make it crash
			// so let's use a random value

			Memory.writeByteArray(buf, [0x85, 0x98, 0x0a, 0xb6, 0x07, 0x5c, 0xc1, 0x97,
										0xab, 0x8d, 0xe0, 0xfa, 0xba, 0x3c, 0x69, 0x96,
										0x82, 0xb4, 0x59, 0x97, 0x93, 0x65, 0x43, 0x51,
										0x44, 0x48, 0x2f, 0x5e, 0xba, 0xe8, 0x21, 0x45])

			return 32
		}
		else {
			return read(fd, buf, count)
		}
	}, 'int', ['int', 'pointer', 'int'])
)
