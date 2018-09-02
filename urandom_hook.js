var openPtr = Module.findExportByName('libc.so', 'open');

// Basically overwrite path if we try to open /dev/urandom
// So the secretKey will be generated from our static file
Interceptor.attach(openPtr, {
	onEnter: function(args) {
		var path = Memory.readUtf8String(args[0])
		if (path == '/dev/urandom') {
			this.path = Memory.alloc(100)
			Memory.writeUtf8String(this.path, '/data/data/com.supercell.clashroyale/fake_dev_urandom')
			args[0] = this.path
		}
	},
	onLeave: function(retval) {}
})