#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import argparse
#from unicorn import *
#from unicorn.arm_const import *
from hexdump import *
#from mxp.hackutils import *
from dxutils import *

def get3AZipPackedFileInfo(fn):
    bs = open(fn,'rb').read()
    header_len = 0x8010
    header = decryptBs(bs[:header_len])
    assert struct.unpack('I', header[:4])[0] == header_len-0x10, 'header failed '
    header = header[0x10:]
    info = []
    offt = header_len
    for o in range(0, len(header), 0x0c):
        try:
            crc, le, off = struct.unpack('III', header[o:o+0xc])
        except struct.error:
            continue
        # if off!=offt: print(f" not ok off {off} {offt} {hex(off)} / {hex(len(bs))}" )
        offt+=le
        if le == 0: continue
        if off+le > len(bs): continue
        if le%0x10 !=0:continue;
        info.append({
                'crc': hex(crc),
                'off': off,
                'len': le,
            })
        fileBs = bs[off:off+le]
        fileContent =  decryptBs(fileBs)
    return info

def get3AImagePackedFileInfo(fn, header_len=0x4b00):
    bs = open(fn,'rb').read()
    header = bs[:header_len]
    info = []
    offt = header_len
    for o in range(0, len(header), 0x0c):
        try:
            crc, le, off = struct.unpack('III', header[o:o+0xc])
        except struct.error:
            continue
        # if off!=offt: print(f" not ok off {off} {offt} {hex(off)} / {hex(len(bs))}" )
        offt+=le
        if le == 0: continue
        if off+le > len(bs): continue
        info.append({
                'crc': hex(crc),
                'off': off,
                'len': le,
            })
    return info

def unpack3AZipFile(f,outDir=None):
    bf = os.path.basename(f);
    if outDir ==None:
        outDir = os.path.dirname(f)
    else:
        df = os.path.join(outDir, bf)
        if not fileExist(df):
            cmd = f'cp {f} {outDir} ' 
            print(runCmd(cmd))
    bs= open(f,'rb').read()
    info  = get3AZipPackedFileInfo(f)
    knowNames = [f for f in open('names').read().splitlines()]
    for t, item in enumerate(info):
        print(item)
        crc = item['crc']
        off = item['off']
        le  = item['len']
        foundName = False
        for name in knowNames:
            if eval(crc) == getFileCrc(name):
                foundName=True;
                break
        if foundName:
            df = os.path.join(outDir, f'{bf}.files', name)
            info[t]['name']=name
        else:
            df = os.path.join(outDir, f'{bf}.files', f"{crc}.bin")
        createDirForFn(df)
        print(off, le, len(bs))
        fileBs = bs[off:off+le]
        fileContent =  decryptBs(fileBs)
        hexdump(fileContent[:0x10])
        print(le, hex(le))
        act_len = struct.unpack('I',fileContent[:4])[0] 
        #assert struct.unpack('I', fileContent[:4])[0] == le-0x10, 'decrypt file failed '
        open(df,'wb').write(fileContent[0x10:0x10+act_len])
    infofn = os.path.join(outDir, f'{bf}.json')
    saveJson2File(info,infofn)
    return info;

def unpack3AImageFile(f,outDir=None, header_len=0x4b00):
    bf = os.path.basename(f);
    if outDir ==None:
        outDir = os.path.dirname(f)
    else:
        df = os.path.join(outDir, bf)
        if not fileExist(df):
            cmd = f'cp {f} {outDir} ' 
            print(runCmd(cmd))
    bs= open(f,'rb').read()
    info  = get3AImagePackedFileInfo(f, header_len)
    knowNames = [f for f in open('names').read().splitlines()]
    for t, item in enumerate(info):
        print(item)
        crc = item['crc']
        off = item['off']
        le  = item['len']
        foundName = False
        for name in knowNames:
            if eval(crc) == getFileCrc(name):
                foundName=True;
                break
        if foundName:
            df = os.path.join(outDir, f'{bf}.files', name)
            info[t]['name']=name
        else:
            #assert False, ' go here '
            df = os.path.join(outDir, f'{bf}.files', f"{crc}.bin")
        createDirForFn(df)
        print(off, le, len(bs))
        fileBs = bs[off:off+le]
        fileContent =  decryptImageData(fileBs)
        open(df,'wb').write(fileContent)
    infofn = os.path.join(outDir, f'{bf}.json')
    saveJson2File(info,infofn)
    return info;


def renameDir(d):
    for f in open('names').read().splitlines():
        crc = getFileCrc(f)
        sf = os.path.join(d, f'{hex(crc)}.bin')
        df = os.path.join(d, f)
        if fileExist(sf):
            cmd = f'mv {sf} {df}'
            print(runCmd(cmd))
    
def unpackAssetFile(f,outDir='/tmp/dumped'):
    info  = unpack3AZipFile(f, outDir);
    bf = os.path.basename(f);
    for item in info:
        name = item['name']
        fn = os.path.join(outDir, f'{bf}.files', name)
        d  = f'{fn}.files'
        createDirIfNeed(d) 
        if name.startswith('libcfg') and name.endswith('.so'):
            cmd = f'cd {d} && tar xvf ../{name}'
            print (runCmd(cmd))
            ifn = os.path.join(d, 'config','images.so')
            unpack3AImageFile(ifn)
        else:                
            print(fn)
            unpack3AImageFile(fn)

def getDataFileInfo(fn):
    bs = open(fn,'rb').read()
    header_len = 0xD4C0
    header = bs[:header_len]
    info = []
    offt = header_len
    for o in range(0, len(header), 0x0c):
        try:
            crc, le, off = struct.unpack('III', header[o:o+0xc])
        except struct.error:
            continue
        # if off!=offt: print(f" not ok off {off} {offt} {hex(off)} / {hex(len(bs))}" )
        print(crc, le, off);
        offt+=le
        if le == 0: continue
        if off+le > len(bs): continue
        if le%0x10 !=0:continue;
        info.append({
                'crc': hex(crc),
                'off': off,
                'len': le,
            })
        #fileBs = bs[off:off+le]
        #fileContent =  (fileBs)
    return info;

    
def unpackDataFile(f,outDir='/tmp/dumped'):
    info  = getDataFileInfo(f);
    bf = os.path.basename(f);
    for item in info:
        continue
        name = item['name']
        fn = os.path.join(outDir, f'{bf}.files', name)
        d  = f'{fn}.files'
        createDirIfNeed(d) 
        if name.startswith('libcfg') and name.endswith('.so'):
            cmd = f'cd {d} && tar xvf ../{name}'
            print (runCmd(cmd))
            ifn = os.path.join(d, 'config','images.so')
            unpack3AImageFile(ifn)
        else:                
            print(fn)
            unpack3AImageFile(fn)
    
    
def main():
    # check file 
    infos = [
        ('bins/had.zip',  '/tmp/dumped/'),
        # ('bins/hadc.zip', '/tmp/dumped/hadc.zip.files'),
        # ('bins/rade.zip', '/tmp/dumped/rade.zip.files'),
    ]
    cmd = 'rm -fr /tmp/dumped/*'
    print(runCmd(cmd))
    for f, d in infos:
        unpackAssetFile(f, d);

def main():
    knowNames = [f for f in open('names').read().splitlines()]
    for root, dir, files in os.walk('/tmp/dumped'):
        for f in files:
            if f.endswith('.json'):
                fn = os.path.join(root, f)
                df = f'{fn[:-5]}.files'
                print(fn, df)
                info = json.load(open(fn))
                for t, item in enumerate(info):
                    crc = item['crc']
                    off = item['off']
                    le  = item['len']
                    if 'name' not in item:
                        for name in knowNames:
                            if eval(crc) == getFileCrc(name):
                                sf = os.path.join(df, f'{crc}.bin')
                                dd = os.path.join(df, name)
                                if fileExist(sf):
                                    print (item, sf, dd)
                                    bs = open(sf,'rb').read()
                                    bs = decryptImageData(bs)
                                    open(dd,'wb').write(bs)
                                    info[t]['name']=name
                                    cmd='rm -f {sf}'
                                    print(runCmd(cmd))
                saveJson2File(info, fn)                    

    
def main():
    # check file 
    infos = [
        ('bins/had.zip',  '/tmp/dumped/'),
        # ('bins/hadc.zip', '/tmp/dumped/hadc.zip.files'),
        # ('bins/rade.zip', '/tmp/dumped/rade.zip.files'),
    ]
    cmd = 'rm -fr /tmp/dumped/*'
    print(runCmd(cmd))
    for f, d in infos:
        unpackAssetFile(f, d);

def pack3AImageFile(f, header_len=0x40000):
    bs = bytearray(b'\0'*header_len)
    info = json.load(open(f'{f}.json'))
    fcnt = 0;
    foffset = header_len;
    hoffset = 0;
    for item in info:
        crc = item['crc']
        fname =  os.path.join(f'{f}.files', f"{crc}.bin")
        if 'name' in item:
            fname =  os.path.join(f'{f}.files', item['name'])
        print(fname, hex(hoffset))
        fbs = decryptImageData(open(fname,'rb').read())
        bs+=fbs
        bs[hoffset:hoffset+0xc]=struct.pack('III', eval(crc), len(fbs), foffset)
        foffset+=len(fbs)
        hoffset+=0x0c
    open(f,'wb').write(bs)

def compress3Alibcfgfile(libcf):
    d = f'{libcf}.files'
    cfiles = []
    for root, dirs, files in os.walk(d):
        for f in files:
            fn = os.path.join(root, f)
            cf = fn[len(d)+1:]
            if os.path.dirname(cf).endswith('.files'):continue
            if cf.endswith('.json'):continue
            cfiles.append(cf)
    cmd = f'cd {d} && tar cvf {libcf} {" ".join(cfiles)}'
    print(runCmd(cmd))

def pack3AZipFile(sf,df, header_len=0x8010):
    headerbs = bytearray(b'\0'*header_len)
    headerbs[:0x10]= struct.pack('IIII', header_len-0x10, 0, 0, 0)
    info = json.load(open(f'{sf}.json'))
    foffset = header_len;
    bs = b""
    hoffset = 0x10;
    for item in info:
        crc = item['crc']
        fname =  os.path.join(f'{sf}.files', f"{crc}.bin")
        if 'name' in item:
            fname =  os.path.join(f'{sf}.files', item['name'])
        obs = open(fname,'rb').read()
        le = len(obs)
        obs = struct.pack('IIII', le, 0, 0, 0)+obs
        fbs = encryptBs(obs)
        bs+=fbs
        headerbs[hoffset:hoffset+0x0c]=struct.pack('III', eval(crc), len(fbs), foffset)
        hoffset+=0x0c
        foffset+=len(fbs)
    print(hex(hoffset))
    open(df,'wb').write(encryptBs(bytes(headerbs))+bs)

def packAssetFile(sf, df):
    sd = f'{sf}.files'
    print(sd)
    if True:
        for root, dirs, files in os.walk(sd):
            for f in files:
                fn = os.path.join(root, f)
                if f == 'images.so':
                    print(fn)
                    pack3AImageFile(fn);
    if True:
        for root, dirs, files in os.walk(sd):
            for f in files:
                fn = os.path.join(root, f)
                if f.startswith('libcfg') and f.endswith('.so'):
                    compress3Alibcfgfile(fn)
    pack3AZipFile(sf,df, header_len=0x8010)


    
def main():
    # d = '/tmp/dumped'; cmd = f'rm -fr {d}/*'; print(runCmd(cmd)); unpackAssetFile('bins/had.zip', d);
    # cmd = ' rm -fr /tmp/dumped1; cp /tmp/dumped /tmp/dumped1 -R -v'; print(runCmd(cmd))

    #packAssetFile('/tmp/dumped1/had.zip', '/tmp/had.zip')

    d = '/tmp/dumped'; cmd = f'rm -fr {d}/*'; print(runCmd(cmd)); unpackAssetFile('bins/had.zip', d);
    unpackAssetFile('bins/hadc.zip', d);
    unpackAssetFile('bins/rade.zip', d);
    #packAssetFile('/tmp/dumped/had.zip', '/tmp/had.zip')
    #packAssetFile('/tmp/dumped/hadc.zip', '/tmp/hadc.zip')
    #packAssetFile('/tmp/dumped/rade.zip', '/tmp/rade.zip')

#def main():
#    f = 'squashfs-root/usr/lib/libdata.so'
#    unpackDataFile(f,outDir='/tmp/dumped')

def main():
    #d = '/tmp/dumped'; cmd = f'rm -fr {d}/*'; print(runCmd(cmd)); unpackAssetFile('bins/dxtest.UIs/had.zip', d);
    #unpackAssetFile('bins/dxtest.UIs/hadc.zip', d);
    #unpackAssetFile('bins/dxtest.UIs/rade.zip', d);

    #packAssetFile('/tmp/dumped/had.zip', '/tmp/had.zip')
    #packAssetFile('/tmp/dumped/hadc.zip', '/tmp/hadc.zip')
    packAssetFile('/tmp/dumped/rade.zip', '/tmp/rade.zip')
                                
def main():
    # d = '/tmp/dumped'; cmd = f'rm -fr {d}/*'; print(runCmd(cmd)); 
    # unpackAssetFile('/media/mxp/DXTEST/roms//had.zip',  d);
    # unpackAssetFile('/media/mxp/DXTEST/roms//hadc.zip', d);
    # unpackAssetFile('/media/mxp/DXTEST/roms//rade.zip', d);

    packAssetFile('/tmp/dumped/had.zip', '/tmp/had.zip')
    packAssetFile('/tmp/dumped/hadc.zip', '/tmp/hadc.zip')
    packAssetFile('/tmp/dumped/rade.zip', '/tmp/rade.zip')

def main():

    parser = argparse.ArgumentParser(description='extractor/packer of assert file of pbdx platform, can not extract and pack simultaneously ')
    parser.add_argument('-e', '--extract', action='store_true', help='extract file', default=False)
    parser.add_argument('-p', '--pack', action='store_true', help='pack file', default=False)
    parser.add_argument('source', help='source')
    parser.add_argument('destine', help='destine')
    args = parser.parse_args()

    if args.extract and not args.pack: 
        print('extrace file ')
        createDirIfNeed(args.destine)
        unpackAssetFile(args.source, args.destine)
    elif not args.extract and args.pack:
        print('pack file ')
        packAssetFile(args.source, args.destine)
    else:
        parser.print_help()

                                

if __name__ == '__main__':
    main()

