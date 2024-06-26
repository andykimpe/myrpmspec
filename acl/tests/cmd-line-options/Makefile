# Copyright (c) 2006 Red Hat, Inc. All rights reserved. This copyrighted material 
# is made available to anyone wishing to use, modify, copy, or
# redistribute it subject to the terms and conditions of the GNU General
# Public License v.2.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# Author: Milos Malik <mmalik@redhat.com>

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Example Makefile for RHTS                                          #
# This example is geared towards a test for a specific package       #
# It does most of the work for you, but may require further coding   #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

# The toplevel namespace within which the test lives.
# FIXME: You will need to change this:
TOPLEVEL_NAMESPACE=CoreOS

# The name of the package under test:
# FIXME: you wil need to change this:
PACKAGE_NAME=acl

# The path of the test below the package:
# FIXME: you wil need to change this:
RELATIVE_PATH=Sanity/cmd-line-options

# Version of the test. Used with make tag.
export TESTVERSION=1.0

# The combined namespace of the test.
export TEST=/$(TOPLEVEL_NAMESPACE)/$(PACKAGE_NAME)/$(RELATIVE_PATH)


# A phony target is one that is not really the name of a file.
# It is just a name for some commands to be executed when you
# make an explicit request. There are two reasons to use a
# phony target: to avoid a conflict with a file of the same
# name, and to improve performance.
.PHONY: all install download clean

# executables to be built should be added here, they will be generated on the system under test.
BUILT_FILES= 

# data files, .c files, scripts anything needed to either compile the test and/or run it.
FILES=$(METADATA) runtest.sh Makefile PURPOSE test-core.sh

run: $(FILES) build
	./runtest.sh

build: $(BUILT_FILES)
	chmod a+x ./runtest.sh ./test-core.sh

clean:
	rm -f *~ *.rpm $(BUILT_FILES)

# You may need to add other targets e.g. to build executables from source code
# Add them here:


# Include Common Makefile
include /usr/share/rhts/lib/rhts-make.include

# Generate the testinfo.desc here:
$(METADATA): Makefile
	@touch $(METADATA)
# Change to the test owner's name
	@echo "Owner:        Milos Malik <mmalik@redhat.com>" > $(METADATA)
	@echo "Name:         $(TEST)" >> $(METADATA)
	@echo "Path:         $(TEST_DIR)" >> $(METADATA)
	@echo "TestVersion:  $(TESTVERSION)" >> $(METADATA)
	@echo "Type:         Sanity" >> $(METADATA)
	@echo "Description:  utilities are tested if they support basic command line options" >> $(METADATA)
	@echo "TestTime:     2m" >> $(METADATA)
	@echo "RunFor:       $(PACKAGE_NAME)" >> $(METADATA)  
# add any other packages for which your test ought to run here
	@echo "Requires:     $(PACKAGE_NAME)" >> $(METADATA)  
# add any other requirements for the script to run here
	@echo "License:      GPLv2" >> $(METADATA)

# You may need other fields here; see the documentation
	rhts-lint $(METADATA)

