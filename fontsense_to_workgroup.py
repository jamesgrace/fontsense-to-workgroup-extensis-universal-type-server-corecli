import os
import errno
import subprocess
import xml.etree.ElementTree as ET
import argparse
from datetime import datetime
from collections import Counter


parser = argparse.ArgumentParser(description='References a text file containing a listing of FontSense checksums and then adds corresponding fonts to a designated UTS Workgroup.')
parser.add_argument("-o", "--output", help="Output folder location ( enquoted + case sensitive absolute path with trailing slash ).")
requiredArgument = parser.add_argument_group('required arguments')
requiredArgument.add_argument("-i", "--input", required=True, help="Input file ( enquoted + case sensitive ) containing list of FontSense IDs.")
requiredArgument.add_argument("-w", "--workgroup", required=True, help="Workgroup ( enquoted + case-sensitive ) within UTS that fonts will be added to.")
arguments = parser.parse_args()


# - - - - - - - - - - - - - - - - - - - - - - - - - version 23june2020 -
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

if arguments.output:
	SESSION_PATH = arguments.output
else:
	SESSION_PATH = os.getcwd()+"/"
TARGET_WORKGROUP = arguments.workgroup
INPUT_FILE = arguments.input

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


# --- [ Counters ] - -

foundFontID = 0
errorFontID = 0
addedToWorkGroup = 0
errorToWorkGroup = 0

# - - - - - - - - - -


# --- [ START ] : Create Session Directory - - - - - - - - - - - - - - - - - - - -
#                 Creates the session directory + redirects stdout to session log

def createSessionDirectory():

	global SESSION_FOLDER
	SESSION_FOLDER = datetime.today().strftime('%m-%d-%Y_%H-%M-%S')

	try:
		os.makedirs(SESSION_PATH+SESSION_FOLDER)

	except OSError:
		if not os.path.exists(SESSION_PATH+SESSION_FOLDER):
			print "\n", "[ ERROR ! ] : Session Path NOT Found !"
			print "[ ------- ] : Verify that the SESSION_PATH value matches an existing folder location...", "\n"
			exit()

	print "\n", "[ START ! ] : Session output logged to [ "+SESSION_PATH+SESSION_FOLDER+"/session_log.txt ]...", "\n"

	import sys
	sys.stdout = open(SESSION_PATH+SESSION_FOLDER+'/session_log.txt', 'w')

# --- [  END  ] : Create Session Directory - - - - - - - - - - - - - - - - - - - -



# --- [ START ] : Get WorkGroups - - - - - - - - - - - - - - - - - - - -
#                 Retrieves an XML tree of the available Workgroups - - -

def getWorkGroups():

	try:
		workgroups_response = subprocess.check_output(["corecli", "-clientserver", "-getWorkgroups"])
#		print(workgroups_response)

	except subprocess.CalledProcessError as error:
		print(error)

	else:
		if '<results-set row-count="0">' in workgroups_response:
			print "\n" , "[ ERROR ! ] : No Workgroups Available !" , "\n"
			exit()

		else:
			workgroups = ET.fromstring(workgroups_response)

			print "\n", "The following Workgroups are available :"
			print "----------------------------------------"

			global workgroup_id
			workgroup_id = None

			columns = workgroups.getiterator('column')

			for row in columns:
				if row.attrib['name'] == "FontWorkgroup__id":
					rowId = row.text
				if row.attrib['name'] == "FontWorkgroup__name":
					rowName = row.text
					print rowName

					if rowName == TARGET_WORKGROUP:
						workgroup_name = rowName
						workgroup_id = rowId

			if workgroup_id is None:
				print "\n", "[ ERROR ! ] : No Matching Workgroup ID Found !"
				print "\n", "[ ------- ] : Verify that the TARGET_WORKGROUP value matches an available Workgroup..." , "\n"
				exit()

			else:
				print "\n", "[ FOUND ! ] : [ Name ] = [", workgroup_name, "] - [ Workgroup ID ] = [", workgroup_id, "]", "\n"
				print "= - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - =", "\n"

# --- [  END  ] : Get WorkGroups - - - - - - - - - - - - - - - - - - - -



# --- [ START ] : Find Font ID - - - - - - - - - - - - - - - - - - - -
#                 Queries for Font Sense Checksum and then retrieves
#                 the corresponding Font ID - - - - - - - - - - - - - -

def findFontID():

	global foundFontID
	global errorFontID

	try:
		with open(INPUT_FILE) as f:
			for checksum in f.read().splitlines():
#				print checksum

				try:
					find_id_response = subprocess.check_output(["corecli", "-clientserver", "-sql", "query=true", "sql=select id from fontface where fontsense_chk = "+checksum])
#					print(find_id_response)

					if '<results-set row-count="1">' in find_id_response:

						fontId = ET.fromstring(find_id_response)

						columns = fontId.getiterator('column')

						for row in columns:
							if row.attrib['name'] == "id":
								rowId = row.text
#								print rowId

								global font_id
								font_id = rowId

						print "[ FOUND ! ] : [ Font Sense Checksum ] = [", checksum, "] - [ Font ID ] = [", font_id, "]", "\n"

						print "\ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ / / / / / / / / / / / / / / / / / / / /", "\n"

						foundFontID += 1

						addFontToWorkGroup(workgroup_id,font_id)

					else:
						if '<results-set row-count="0">' in find_id_response:

							print "[ ERROR ! ] : [ Font Sense Checksum ] = [", checksum, "] - No Matching Font ID Found !", "\n"

							errorFontID += 1

				except subprocess.CalledProcessError as error:
					print(error)

	except IOError:
		print "[ ERROR ! ] : Input File NOT Found !"
		print "[ ------- ] : Verify that the INPUT_FILE value matches an existing text file..."

	finally:
		f.close()

# --- [  END  ] : Find Font ID - - - - - - - - - - - - - - - - - - - - - - - - - -



# --- [ START ] : Add Font To WorkGroup  - - - - - - - - - - - - - - - - - - - -

def addFontToWorkGroup(workgroup_id,font_id):

	global addedToWorkGroup
	global errorToWorkGroup

	try:
		addfont_response = subprocess.check_output(["corecli", "-clientserver", "-addFontsToWorkgroup", "fontIds="+font_id, "workgroupId="+workgroup_id])
#		print(addfont_response)

		if 'success.ok' in addfont_response:

			print "[ ADDED ! ] : [ Font ID ] = [", font_id, "] >>> Added To >>> [ Workgroup ID ] = [", workgroup_id, "]", "\n"

			addedToWorkGroup +=1

		else:

			print "[ ERROR ! ] : [ Font ID ] = [", font_id, "] - NOT Added To - [ Workgroup ID ] = [", workgroup_id, "]", "\n"

			errorToWorkGroup +=1

	except subprocess.CalledProcessError as error:
		print(error)

	print "= - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - =", "\n"

# --- [  END  ] : Add Font To WorkGroup - - - - - - - - - - - - - - - - - - - -



# --- [ START ] : Job Summary - - - - - - - - - - - - - - - - - - - - - - - - -

def jobSummary():

	print "+ - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - +", "\n"
	print "| - - - - - - - - - - - - - - -  J O B   L O G  - - - - - - - - - - - - - - - |", "\n"
	print "+ - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - +", "\n"
	print " [", foundFontID, "] fonts found and [", errorFontID, "] fonts NOT found.", "\n"
	print " [", addedToWorkGroup, "] fonts added to the [", TARGET_WORKGROUP, "] Workgroup (", errorToWorkGroup, "errors ).", "\n"
	print "+ - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - +", "\n"

# --- [  END  ] : Job Summary - - - - - - - - - - - - - - - - - - - - - - - - -



createSessionDirectory()

getWorkGroups()

findFontID()

jobSummary()
