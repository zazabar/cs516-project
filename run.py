"""
run.py
Scope: The entrance point for our program.
Authors: Jeffrey Smith, Bill Cramer, Evan French
"""
import sys, getopt

def main():
	"""
	Main function of the application. Call -h or --help for command line inputs.
	"""
	mode, inputDirectory, annotationsDirectory, outputDirectory, modelFile = None, None, None, None, None
	
	#Process command line entries.
	opts, args = getopt.getopt(sys.argv[1:], 'm:i:o:d:a:h',["mode=","input=","output=","model=","annotations=","help"])
	for opt, arg, in opts:
		if opt in ("-m","--mode"):
			mode = arg
		elif opt in ("-i","--input"):
			inputDirectory = arg
		elif opt in ("-o","--output"):
			outputDirectory = arg
		elif opt in ("-d","--model"):
			modelFile = arg
		elif opt in ("-a","--annotations"):
			annotationsDirectory = arg
		elif opt in ("-h","--help"):
			printHelp()
			return
		
	#Verify if needed command line entries are present.
	if mode == None:
		print("You must specify a mode to use with -m or --mode. Options are train, test, and eval.")
		return
	elif mode == "eval" and modelFile == None:
		print("You must specify a model to use for evaluation using -d or --model.")
		
	if inputDirectory == None:
		print("You must specify a directory with input files with -i or --input.")
		return

	if annotationsDirectory == None:
		print("You must specify a directory with annotation files with -a or --annotations.")
		return
		
	if outputDirectory == None:
		print("You must specify a directory for output files with -o or --output.")
		return
		
def printHelp():
	"""
	Prints out the command line help information.
	"""	
	print("Options:")
	print("-m/--mode [test,train,eval] : Specify the mode of the system.")
	print("-i/--input DIR : Specify the input directory to read from.")
	print("-a/--annotations DIR : Specify the annotations directory to read from.")
	print("-o/--output DIR : Specify the output directory to write to.")
	print("-d/--model FILE : Specify a model to use when running in eval mode.")
	
	return

if __name__ == "__main__":
	main()