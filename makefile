all: update_mds

update_mds:
	source env/bin/activate && src/update_from_pocket.py && git add . && git commit -m "auto update" && git git push origin master