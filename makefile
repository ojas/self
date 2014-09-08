all: update_mds

update_mds:
	source env/bin/activate && src/update_from_pocket.py && git add *.md && git commit -m "auto update" && git push origin master