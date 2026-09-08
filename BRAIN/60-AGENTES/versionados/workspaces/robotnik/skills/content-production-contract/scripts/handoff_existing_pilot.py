#!/usr/bin/env python3
"""Owner-operated, task-bound PNG handoff. No path arguments or elevated helper.

Authority: Hebert's scoped 2026-09-08 resumption. Never a sandbox workaround
available to the agent. Exact completed thread outputs only; no credentials.
"""
import hashlib
import json
import os
from pathlib import Path
import stat
import struct
import subprocess
import sys
import zlib

SOURCE = '/data/.openclaw/agents/robotnik/codex-home/generated_images/01a0813c-b8ba-7a61-864d-70849ea46469'
DEST = '/data/.openclaw/workspace-robotnik/entregas/piloto-contrato-criativo-v1-20260908/native-candidates'
MAX = 25 * 1024 * 1024
CATALOG = {'call_lnH8JMFkBZTogapfDcRYdpAC.png': (1733275, 'b64f50d45d2db4f5630efbe7c944742bc8e33e120381c52dd5d5225ce31ec3d0'), 'call_r3CVYFM1hEuDwtkhK7G8rMyH.png': (1644245, 'd1fe2c7dd5dccd71892293276fc7bff51d0f1a12ba2035cf8f0e088ea50cf472'), 'exec-204dfe6d-7f53-47ca-b95d-6413a2335b32.png': (1703571, '652e13aee8a1ccef33921663380c3baa6a0ead223d2f2f4bdcfcd83881469963'), 'exec-2482dfb3-4c88-4b3b-a84f-a769c29dac95.png': (1706426, 'eb73f0073fede6a982a33853f2d628ebc0ed83743abc260264425eb1acd34726'), 'exec-754ebc7d-df34-47dd-aa14-de472549d283.png': (1730527, '2dbced83c2e5ae7b0b71495a550e8fbe2ccb0934320004338a80c3c2feeafa7f'), 'exec-f152ae97-4d92-4e86-b5d8-fb3d4d572fcb.png': (1729715, '18b4bc35db720c05febdb608d327866f034d40eb673f67638db11b8ba6e2e1fd'), 'exec-f8626450-f975-42b7-bc6a-2021f814e534.png': (1740148, 'a3cd85c02e21a7572a93937d45d651c883bdca4142de91cb2caa25fab618c9a6')}  # Frozen from completed native outputs during authorized reconciliation.

def directory(path):
    """Open every directory component without following symbolic links."""
    if not path.startswith('/') or any(p in ('.', '..') for p in path.split('/')):
        raise ValueError('invalid directory')
    fd = os.open('/', os.O_RDONLY | os.O_DIRECTORY)
    try:
        for part in path.split('/')[1:]:
            if not part:
                raise ValueError('empty component')
            nxt = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=fd)
            os.close(fd)
            fd = nxt
        return fd
    except BaseException:
        os.close(fd)
        raise

def png(data):
    if not 0 < len(data) <= MAX or data[:8] != b'\x89PNG\r\n\x1a\n':
        raise ValueError('size or PNG signature')
    pos = 8
    dimensions = None
    ended = False
    while pos < len(data):
        if pos + 12 > len(data):
            raise ValueError('truncated chunk')
        length = struct.unpack('>I', data[pos:pos+4])[0]
        end = pos + 12 + length
        if end > len(data):
            raise ValueError('truncated chunk body')
        kind = data[pos+4:pos+8]
        body = data[pos+8:pos+8+length]
        if zlib.crc32(kind + body) & 0xffffffff != struct.unpack('>I', data[end-4:end])[0]:
            raise ValueError('CRC mismatch')
        if pos == 8:
            if kind != b'IHDR' or length != 13:
                raise ValueError('missing IHDR')
            dimensions = struct.unpack('>II', body[:8])
            if not all(0 < d <= 4096 for d in dimensions):
                raise ValueError('oversized dimensions')
        pos = end
        if kind == b'IEND':
            if length or pos != len(data):
                raise ValueError('invalid IEND or trailing bytes')
            ended = True
    if not ended:
        raise ValueError('incomplete PNG')
    subprocess.run(['/usr/bin/convert', '-regard-warnings', '-limit', 'memory', '128MiB',
                    '-limit', 'map', '256MiB', '-limit', 'disk', '0', 'png:-', 'null:'],
                   input=data, capture_output=True, check=True, timeout=20)
    return dimensions

def read_candidate(fd, name, expected):
    if '/' in name or '\\' in name or '..' in name or not name.endswith('.png'):
        raise ValueError('invalid basename or extension')
    f = os.open(name, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=fd)
    try:
        before = os.fstat(f)
        if not stat.S_ISREG(before.st_mode) or before.st_nlink != 1:
            raise ValueError('not a unique regular file')
        if not 0 < before.st_size <= MAX:
            raise ValueError('empty or oversized')
        chunks = []
        total = 0
        while True:
            b = os.read(f, min(1048576, MAX + 1 - total))
            if not b:
                break
            chunks.append(b)
            total += len(b)
            if total > MAX:
                raise ValueError('grew oversized')
        data = b''.join(chunks)
        after = os.fstat(f)
        fingerprint = lambda s: (s.st_dev, s.st_ino, s.st_size, s.st_mtime_ns, s.st_ctime_ns)
        if fingerprint(before) != fingerprint(after):
            raise ValueError('source changed during read')
        digest = hashlib.sha256(data).hexdigest()
        if (len(data), digest) != tuple(expected):
            raise ValueError('not frozen completed output')
        dimensions = png(data)
        return data, dict(bytes=len(data), sha256=digest, dimensions=dimensions,
                          source_uid=before.st_uid, source_gid=before.st_gid,
                          source_mode=oct(stat.S_IMODE(before.st_mode)))
    finally:
        os.close(f)

def main():
    if len(sys.argv) != 1 or os.geteuid() != 0:
        raise SystemExit('Owner execution only; no arguments accepted')
    src = directory(SOURCE)
    # Output is a fixed existing task directory, never chosen by a caller.
    dst = directory(DEST)
    receipts = []
    try:
        for name, expected in CATALOG.items():
            data, receipt = read_candidate(src, name, expected)
            if (receipt['source_uid'], receipt['source_gid']) != (1000, 1000):
                raise ValueError('unexpected source owner')
            try:
                existing, _ = read_candidate(dst, name, expected)
                assert existing == data
                state = 'RECONCILED_EXISTING'
            except FileNotFoundError:
                temp = '.' + name + '.pending'
                f = os.open(temp, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600, dir_fd=dst)
                try:
                    os.fchown(f, 1000, 1000)
                    with os.fdopen(f, 'wb', closefd=False) as stream:
                        stream.write(data)
                        stream.flush()
                        os.fsync(f)
                    # Atomic no-overwrite publication. Never replace existing artwork.
                    os.link(temp, name, src_dir_fd=dst, dst_dir_fd=dst, follow_symlinks=False)
                finally:
                    os.close(f)
                    os.unlink(temp, dir_fd=dst)
                os.fsync(dst)
                state = 'EXPORTED'
            ds = os.stat(name, dir_fd=dst, follow_symlinks=False)
            receipt.update(source=SOURCE+'/'+name, destination=DEST+'/'+name, status=state,
                           destination_uid=ds.st_uid, destination_gid=ds.st_gid,
                           destination_mode=oct(stat.S_IMODE(ds.st_mode)))
            receipts.append(receipt)
        print(json.dumps(receipts, indent=2))
    finally:
        os.close(src)
        os.close(dst)

if __name__ == '__main__':
    main()
