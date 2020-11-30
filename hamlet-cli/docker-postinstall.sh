# stash files to prevent deletion when host volume mounts
# useful when you want to break stuff using your favorite editor
# which is not vim or emac.
echo "Moving /opt/hamlet => /hamlet to prevent overriding by volume"
mv /opt/hamlet /hamlet
echo "Current /hamlet content"
tree /hamlet -L 2

mkdir -p /hamlet-cli/.cmdb
