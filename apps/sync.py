from subprocess import call

call('sudo service ntp stop', shell=True)
call('sudo ntpdate 0.pool.ntp.org', shell=True)
call('sudo service ntp start', shell=True)

print("Time Updated.")