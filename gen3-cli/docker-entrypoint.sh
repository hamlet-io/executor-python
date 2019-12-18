# clearing previos version
echo "Current /opt/codeontap volume state"
tree -L 2 /opt
echo "Removing old files"
rm -rf /opt/codeontap/*
# moving stashed version to GENERATION_DIR
echo "Moving actual files back into /opt/codeontap"
mv /codeontap/* /opt/codeontap
echo "Changing files mode to 777"
chmod -R 777 /opt/codeontap
# just waiting forever
echo "Waiting forever..."
tail -f -s 60 /dev/null
