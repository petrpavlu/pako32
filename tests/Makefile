# Copyright (C) 2023 Petr Pavlu <petr.pavlu@dagobah.cz>
# SPDX-License-Identifier: MIT

SUBDIRS := $(filter-out __pycache__,$(patsubst ./%/,%,$(filter %/, $(wildcard ./*/))))

.PHONY: all $(SUBDIRS)
all: $(SUBDIRS)
$(SUBDIRS):
	$(MAKE) -C $@ all

SUBCLEAN = $(addsuffix .clean, $(SUBDIRS))

.PHONY: clean $(SUBCLEAN)
clean: $(SUBCLEAN)
$(SUBCLEAN): %.clean:
	$(MAKE) -C $* clean

