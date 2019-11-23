# clearing previos version
rm -rf /opt/codeontap/*
# moving stashed version to GENERATION_DIR
mv /codeontap/* /opt/codeontap
# just waiting forever
tail -f -s 60 /dev/null
