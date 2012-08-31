#!/usr/bin/env python
'''
Execute like: $CINGROOT/python/cing/Scripts/vCing/Utils.py
or execute from vCing.py
'''

from cing.Libs.disk import * #@UnusedWildImport
import commands

def prepareMaster(master_target_dir, doClean=False):
    "Return True on error."
    cwd = os.getcwd()
    if not os.path.exists(master_target_dir):
        # Setup in April 2011. Where XXXXXX is the not to be committed pool id.
#            jd:dodos/vCingSlave/ pwd
#            /Library/WebServer/Documents/tmp/vCingSlave
#            jd:dodos/vCingSlave/ ls -l
#            lrwxr-xr-x  1 jd  admin  18 Apr 15 21:39 vCingXXXXX@ -> /Volumes/tetra/vCingXXXXX
        print "Creating path that probably should be created manually because it might be an indirect one: %s" % master_target_dir
        mkdirs(master_target_dir)
    if not os.path.exists(master_target_dir):
        print "ERROR: Failed to create: " + master_target_dir
        return True
    os.chdir(master_target_dir)
    for d in 'log log2 result'.split():
        if doClean:
            print "DEBUG: Removing and recreating %s" % d
            rmdir(d)
        else:
            print "DEBUG: Creating if needed %s" % d
        mkdirs(d)
    # end for
    os.chdir(cwd)
# end def

def onEachSlave( cmd='uptime', slaveListFile="slaveList.py"):
    
    slaveList = []
    slaveList += [ '145.100.57.%s' % x for x in range(6,7) ]
#    slaveList += [ '145.100.58.%s' % x for x in range(41,46) ]
#    slaveList += [ '145.100.58.%s' % x for x in range(47,51) ]
#    slaveList += [ '145.100.58.%s' % x for x in range(52,56) ]
#    slaveList += [ '145.100.58.%s' % x for x in range(57,61) ]
#    slaveList += [ '145.100.58.%s' % x for x in range(62,64) ]
#    slaveList += [ '145.100.58.%s' % x for x in range(65,78) ]
#    slaveList += [ '145.100.58.%s' % x for x in range(79,81) ]
#    slaveList += [ '145.100.58.%s' % x for x in range(85,97) ]
    coresTotal = 12*0 + 0*8*8 + 1*4
#    slaveList += [ '145.100.57.%s' % x for x in range(244,252) ]
#    slaveList += [ '145.100.57.%s' % x for x in [221,210,212] ]
    # Disable some security checks.
    n = len(slaveList)
    print "there are %8d slaves" % n
    print "there are %8d cores" % coresTotal
    print "there are %8.3f cores/slave" % (coresTotal / n)
    sshOptionList = '-o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no'
    sshOptionList += ' -q'
    i = 0
    for slave in slaveList:
        i += 1
        cmdComplete = 'ssh %(sshOptionList)s i@%(slave)s %(cmd)s' % {                                                             
                'sshOptionList':sshOptionList, 'slave':slave, 'cmd':cmd}
        status, result = commands.getstatusoutput(cmdComplete)
        if not status:
            print "%3d %s %s" % (i, slave, result)
            continue
        # end if
        print "%3d %s %s" % (i, slave, "ERROR: Failed command: %s with status: %s with result: %s, now sleeping a short while." % (
            cmd, status, result))
        time.sleep(1)        
    # end for    
# end def
    
if __name__ == "__main__":
    if False:
        if prepareMaster(sys.argv[1]):
            print "ERROR: Failed to prepareMaster"
        # end if
    # end if
    if 1:    
        if onEachSlave():
            print "ERROR: Failed to prepareMaster"
        # end if
    # end if
# end if
        