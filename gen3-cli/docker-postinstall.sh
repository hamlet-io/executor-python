# stash files to prevent deletion when host volume mounts
# useful when you want to break stuff using your favorite editor
# which is not vim or emac.
echo "Moving /opt/codeontap => /codeontap to prevent overriding by volume"
mv /opt/codeontap /codeontap
echo "Current /codeontap content"
tree /codeontap -L 2
# make a command from a test module, just for demo purposes
echo "Creating cot-tescases bin file"
ln -s /gen3-cli/cot-testcase.sh /bin/cot-testcases
