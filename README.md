# vManageUtilityScripts
Python scripts to help copy Feature Templates across vManage controllers using REST APIs of vManage

# Prerequisites
- Python v3
- Install pip packages mentioned in requirements.txt

# Python Script(s)
- copy_vmanage_feature_template.py is used to copy the vManage feature template from vManage-1 (SRC_VMANAGE entry in config.ini) to vManage-2 (DEST_VMANAGE entry in config.ini)
The script takes in templateName as an argument in the format "-template templateName"

# Note
Please make sure that the versions of the source and the destination vManage controllers are the same, as the template contents may vary based on the feature set supported in the specific version
