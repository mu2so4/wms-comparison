echo "Clonning galaxy git repository"
git clone https://github.com/galaxyproject/galaxy.git

echo "Copping tools conifguration"
cp tool_conf.xml.sample ./galaxy/config/

echo "Copping galaxy tools"
cp -r seismic ./galaxy/tools
cp -r image_processing ./galaxy/tools

echo "Run galaxy"
sh ./galaxy/run.sh