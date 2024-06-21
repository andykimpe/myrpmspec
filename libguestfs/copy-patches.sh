#!/bin/bash -

set -e

# Maintainer script to copy patches from the git repo to the current
# directory.  Use it like this:
#   ./copy-patches.sh

# Check we're in the right directory.
if [ ! -f libguestfs.spec ]; then
    echo "$0: run this from the directory containing 'libguestfs.spec'"
    exit 1
fi

git_checkout=$HOME/d/libguestfs-rhel-6.6
if [ ! -d $git_checkout ]; then
    echo "$0: $git_checkout does not exist"
    echo "This script is only for use by the maintainer when preparing a"
    echo "libguestfs release on RHEL."
    exit 1
fi

# Get the base version of libguestfs.
version=`grep '^Version:' libguestfs.spec | awk '{print $2}'`

# Remove any existing patches.
git rm -f [0-9]*.patch ||:
rm -f [0-9]*.patch

# Get the patches.
(cd $git_checkout; rm -f [0-9]*.patch; git format-patch $version)
mv $git_checkout/[0-9]*.patch .

# Remove any not to be applied.
rm -f *NOT-FOR-RPM*.patch

# Add the patches.
git add [0-9]*.patch

# Print out the patch lines.
echo
echo "--- Copy the following text into libguestfs.spec file"
echo

rhel_6_flag=no
echo "# Feature and backport patches."
for f in [0-9]*.patch; do
    n=`echo $f | awk -F- '{print $1}'`
    is_rhel_6=no
    if [ "$(echo $f | awk -F- '{print $2 $3}')" = "RHEL6" ]; then
	is_rhel_6=yes
    fi
    if [ "$rhel_6_flag" = "no" -a "$is_rhel_6" = "yes" ]; then
	echo
	echo "# RHEL 6 specific patches."
	rhel_6_flag=yes
    elif [ "$rhel_6_flag" = "yes" -a "$is_rhel_6" = "no" ]; then
	echo "$0: error: patch out of order near $f"
	exit 1
    fi
    echo "Patch$n:     $f"
done

echo
echo "--- End of text"