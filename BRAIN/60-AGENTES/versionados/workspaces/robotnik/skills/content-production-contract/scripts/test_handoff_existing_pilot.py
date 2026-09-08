import hashlib
import os
from pathlib import Path
import struct
import subprocess
import tempfile
import unittest
import zlib
import handoff_existing_pilot as h

class BoundaryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.base = Path(self.tmp.name)
        self.fd = h.directory(str(self.base))
        self.good = subprocess.check_output(['/usr/bin/convert', '-size', '4x4', 'xc:white', 'png:-'])
    def tearDown(self):
        os.close(self.fd)
        self.tmp.cleanup()
    def read(self, data, name='x.png'):
        (self.base/name).write_bytes(data)
        return h.read_candidate(self.fd, name, (len(data), hashlib.sha256(data).hexdigest()))
    def test_valid(self):
        self.assertEqual(self.read(self.good)[1]['dimensions'], (4, 4))
    def test_empty(self):
        with self.assertRaises(ValueError): self.read(b'')
    def test_signature(self):
        with self.assertRaises(ValueError): self.read(b'not a PNG')
    def test_partial(self):
        with self.assertRaises(ValueError): self.read(self.good[:-8])
    def test_trailing(self):
        with self.assertRaises(ValueError): self.read(self.good+b'x')
    def test_extension(self):
        with self.assertRaises(ValueError): self.read(self.good, 'x.jpg')
    def test_traversal(self):
        for name in ['../x.png', '/tmp/x.png', 'a/x.png', 'a\\x.png']:
            with self.assertRaises(ValueError): h.read_candidate(self.fd, name, (0,''))
    def test_symlink_file(self):
        (self.base/'real.png').write_bytes(self.good)
        (self.base/'x.png').symlink_to(self.base/'real.png')
        with self.assertRaises(OSError): h.read_candidate(self.fd,'x.png',(len(self.good),hashlib.sha256(self.good).hexdigest()))
    def test_symlink_directory(self):
        (self.base/'real').mkdir()
        (self.base/'link').symlink_to(self.base/'real',target_is_directory=True)
        with self.assertRaises(OSError): h.directory(str(self.base/'link'))
    def test_directory_leaf(self):
        (self.base/'x.png').mkdir()
        with self.assertRaises(ValueError): h.read_candidate(self.fd,'x.png',(0,''))
    def test_fifo(self):
        os.mkfifo(self.base/'x.png')
        with self.assertRaises(ValueError): h.read_candidate(self.fd,'x.png',(0,''))
    def test_hardlink(self):
        (self.base/'real.png').write_bytes(self.good)
        os.link(self.base/'real.png',self.base/'x.png')
        with self.assertRaises(ValueError): h.read_candidate(self.fd,'x.png',(0,''))
    def test_oversized(self):
        with (self.base/'x.png').open('wb') as f: f.truncate(h.MAX+1)
        with self.assertRaises(ValueError): h.read_candidate(self.fd,'x.png',(h.MAX+1,''))
    def test_unrecorded_hash(self):
        (self.base/'x.png').write_bytes(self.good)
        with self.assertRaises(ValueError): h.read_candidate(self.fd,'x.png',(len(self.good),'0'*64))
    def test_decode_failure(self):
        def chunk(k,b): return struct.pack('>I',len(b))+k+b+struct.pack('>I',zlib.crc32(k+b)&0xffffffff)
        bad=b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('>IIBBBBB',4,4,8,2,0,0,0))+chunk(b'IDAT',b'bad deflate')+chunk(b'IEND',b'')
        with self.assertRaises(subprocess.CalledProcessError): self.read(bad)
    def test_cli_no_arbitrary_paths(self):
        p=subprocess.run(['python3',h.__file__,'/tmp/arbitrary.png'],capture_output=True)
        self.assertNotEqual(p.returncode,0)

if __name__=='__main__': unittest.main()
