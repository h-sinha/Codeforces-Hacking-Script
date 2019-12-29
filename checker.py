# parameters expected output, actual output
def Checker(test_output, output):
	print(test_output, output)
	for i in range(len(test_output)):
		# outputs don't match so hack!!
		if test_output[i] != output[i]:
			print(test_output, output)
			return 1
	return 0