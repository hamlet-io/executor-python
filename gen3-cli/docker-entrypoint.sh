# clearing previos version
echo "Current /opt/hamlet volume state"
tree -L 2 /opt
echo "Removing old files"
rm -rf /opt/hamlet/*
# moving stashed version to GENERATION_DIR
echo "Moving actual files back into /opt/hamlet"
mv /hamlet/* /opt/hamlet
echo "Changing files mode to 777"
chmod -R 777 /opt/hamlet
# just waiting forever
echo "Waiting forever..."
tail -f -s 60 /dev/null
