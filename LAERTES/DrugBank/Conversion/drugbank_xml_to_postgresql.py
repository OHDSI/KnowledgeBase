#
# The purpose of this file is to convert XML data from DrugBank
# into PostgreSQL which can easily be uploaded to an object-relational
# database.
#

import os
import sys
import xml.etree.ElementTree as ET

source_xml_file = 'drugbank.xml'