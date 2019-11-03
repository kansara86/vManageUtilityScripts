## vManageUtilityScripts
Python scripts to help copy Feature Templates across vManage controllers using its REST APIs

* Technology stack: Primary programming language Python3. The code is intended to be used as a standalone script with the modules used defined in requirements.txt
* Status:  Beta

## Use Case Description

While working with feature templates with multiple vManage controllers, one of the most common tasks is to copy the feature templates from 1 controller to another. This script helps to copy the feature templates contents across the vManage controllers.

## Installation

* Python version: Python3
* Install the packages mentioned in requirements.txt using 'pip install -r requirements.txt'

## Usage

* copy_vmanage_feature_template.py is the main python script used to copy the vManage feature template from vManage-1 (SRC_VMANAGE entry in config.ini) to vManage-2 (DEST_VMANAGE entry in config.ini)
* config.ini file has the host and user details for the vManage controllers. The source vManage controller details are stored in SRC_VMANAGE, and destination vManage controller details are stored in DEST_VMANAGE
* The feature template to be copied needs to be passed in as an argument
* From the root directory run the command 'python3 copy_vmanage_feature_template.py -template {templateName}'. For example, feature template SNMP_Template can be copied across using the command 'python3 copy_vmanage_feature_template.py -template SNMP_Template'

## Known issues

Please make sure that the versions of the source and the destination vManage controllers are the same, as the template contents may vary based on the feature set supported in the specific version

## Getting help

If you have questions, concerns, bug reports, etc., please create an issue against this repository.

## Getting involved

If you want to extend the scripts beyond feature templates, please push the changes to this repository in a new branch and create a Pull Request. Changes will be reviewed and then merged to develop branch

[![published](https://static.production.devnetcloud.com/codeexchange/assets/images/devnet-published.svg)](https://developer.cisco.com/codeexchange/github/repo/kansara86/vManageUtilityScripts)