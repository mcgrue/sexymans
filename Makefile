# Makefile
# Copyright 2008, Sean B. Palmer, inamidst.com
# Licensed under the Eiffel Forum License 2.

archive: ;
	# hg archive -t tbz2 phenny-hg.tar.bz2
	git archive --format=tar --prefix=phenny/ HEAD | bzip2 > phenny.tar.bz2

ci: ;
	# hg ci
	git commit -a && git push origin master

log: ;
	# git log --date=short --format='%h %ad %s'
	git graph

# Anything below here is added by eeeady for the purposes of configuring mcgrue/sexymans
update: ;
	git pull origin/master 

install-upstart: ;
	install -o root -g root -m 0644 config/sexymans.conf /etc/init/sexymans.conf

install-upstart: ;
    # This only works on a linux box with upstart
    install -o root -g root -m 0644 config/sexymans.conf /etc/init/sexymans.conf
