"""
process_annotations.py
Scope: Process an existing annotation file by comparing the annotated labels with predicted labels using MetaMap.
    Annotations with matching labels will be saved to a new file as gold standard training data.
Authors: Jeffrey Smith, Bill Cramer, Evan French
"""
import sys, getopt, os, re
import metamap_helpers
from classes import Annotation

def main():
    """
	Main function of the application. Call -h or --help for command line inputs.
	"""
    metamap_path, ann_path, gold_ann_path, save_failed = None, None, None, None

    #Process command line entries.
    opts, args = getopt.getopt(sys.argv[1:], 'm:a:g:s:h',["metamap=","ann_path=","gold_ann_path=","save_failed=","help"])
    for opt, arg, in opts:
        if opt in ("-m","--metamap"):
            metamap_path = arg
        elif opt in ("-a","--ann_path"):
            ann_path = arg
        elif opt in ("-g","--gold_ann_path"):
            gold_ann_path = arg
        elif opt in ("-s","--save_failed"):
            save_failed = arg
        elif opt in ("-h","--help"):
            printHelp()
            return

    #Verify if needed command line entries are present.
    if metamap_path == None:
        print("You must specify a path to your MetaMap installation with -m or --metamap. Path must be absolute (i.e. '/opt/public_mm/bin/metamap12').")
        return
    if ann_path == None:
        print("You must specify a directory containing annotation files with -a or --ann_path.")
        return
    if gold_ann_path == None:
        print("You must specify a directory in which gold standard annotation files should be output with -g or --gold_ann_path.")
        return
    if save_failed == None:
        save_failed = False

    #Process the annotations
    ProcessAnnotations(metamap_path, ann_path, gold_ann_path, save_failed)

#Author: Evan French
def printHelp():
	"""
	Prints out the command line help information.
	"""	
	print("Options:")
	print("-m/--metamap DIR : Specify the absolute path of your MetaMap installation (i.e. '/opt/public_mm/bin/metamap12').")
	print("-a/--annotation_path DIR : Specify the directory containing annotation files.")
	print("-g/--gold_ann_path DIR : Specify the directory in which the gold standard annotations should be output.")
	print("-s/--save_failed [True, False] : Should files be created for non-gold standard annotations? ")
	
	return

#Author: Evan French
def ProcessAnnotations(metamap_path, ann_path, gold_ann_path, save_failed = False):
	"""
	Uses MetaMap to corroborate annotations. Annotations where the label on the annotation
	and the label predicted by MetaMap are in agreement are saved to a file with the same name
	in the directory specified by gold_ann_path

	@param metamap_path: Path to MetaMap installation
	@param ann_path: Path to annotation directory
	@param gold_ann_path: Path path for newly identified gold standard annotations
	@param save_failed: Save failed annotations to their own separate file for reference, defaults to false
	"""

	cwd = os.getcwd()
	os.chdir(ann_path)

	#Create output directory for newly identified gold standard annotations if it doesn't exist
	if not os.path.exists(gold_ann_path):
		os.makedirs(gold_ann_path)

	#Create output directory for non-gold annotations if save_failed parameter is True
	failed_path = os.path.join(gold_ann_path, "failed")
	if save_failed and not os.path.exists(failed_path):
		os.makedirs(failed_path)

	#Iterate over documents in the ann_path directory
	for document in [f for f in os.listdir() if os.path.isfile(f)]:

		#Strip the extension from the file to get the document name
		docName = os.path.splitext(document)[0]
			
		#Instantiate a list to hold Annotations for each document
		annotationList = []
		goldList = []
		failedList = []

		#Create an Annotation object for each line in the document and append the concepts to a list
		doc = open(document, "r")  
		for line in doc.readlines():
			an = Annotation(line)
			annotationList.append(an)
		doc.close()
		
		#Run pymetamap over annotations and return semantic types
		annotated_concepts = [a.concept for a in annotationList]
		mmSemTypes = metamap_helpers.GetMetaMapSemanticTypes(metamap_path, annotated_concepts)
		
		#Check MetaMap prediction vs annotation label
		for ix, annotation in enumerate(annotationList):
			isGold, prediction = metamap_helpers.CheckAnnotationAgainstSemTypes(annotation, mmSemTypes[ix])
			
			#If metamap and annotation file agree, add to gold standard list
			if isGold:
				goldList.append(annotation.original)
			elif save_failed:
				failedList.append(prediction + ' ' + annotation.original)
		
		#Write new gold standard annotations to a new file
		new_gold_file = os.path.join(gold_ann_path, docName + ".con")
		with open(new_gold_file, 'w') as f:
			for item in goldList:
				f.write(item)

		#Write non-gold annotations to a new file if save_failed = True
		if save_failed:
			new_failed_file = os.path.join(failed_path, docName + ".con")
			with open(new_failed_file, 'w') as f:
				for item in failedList:
					f.write(item)
		
	#Return to the original directory
	os.chdir(cwd)

if __name__ == "__main__":
	main()
