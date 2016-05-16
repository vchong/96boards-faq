#
# Split out pages from the FAQ nursery ready to copy to wordpress
#

MD = $(subst README.md,,$(wildcard *.md))
HTML = $(MD:%.md=%.html)
WP = $(HTML:%.html=%.wp)

all : 96boards-wiki
	cd 96boards-wiki && git pull
	python split-topics.py 96boards-wiki/The-FAQ-nursery.md
	$(MAKE) _all

# We need to do a double level make to ensure the wildcards get
# re-evaluated after we split out the topics from the wiki.
_all : $(WP)

96boards-wiki :
	git clone https://github.com/96boards/documentation.wiki 96boards-wiki

clean :
	$(RM) $(MD) $(HTML)

%.html : %.md
	cmark $< > $@

%.wp : %.html
	python wordpressify.py $< > $@
