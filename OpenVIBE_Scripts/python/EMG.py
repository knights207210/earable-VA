import numpy

class EMGOVBox(OVBox):
	def __init__(self):
		OVBox.__init__(self)
		self.signalHeader = None
		EMGOVBox.count = 0
		EMGOVBox.keepState = 0
		EMGOVBox.droneTakeOff = 0
		EMGOVBox.forwardPrevTime = 0

	def process(self):
		for chunkIndex in range( len(self.input[0]) ):
			if(type(self.input[0][chunkIndex]) == OVSignalHeader):
				self.signalHeader = self.input[0].pop()

				outputHeader = OVSignalHeader(
				self.signalHeader.startTime, 
				self.signalHeader.endTime, 
				[1, self.signalHeader.dimensionSizes[1]], 
				['Mean']+self.signalHeader.dimensionSizes[1]*[''],
				self.signalHeader.samplingRate)

				self.output[0].append(outputHeader)
				
			elif(type(self.input[0][chunkIndex]) == OVSignalBuffer):
				chunk = self.input[0].pop()
				EMG1 = chunk[0:32]	# Fp1
				EMG2 = chunk[32:64]	# Fp2
				# range1 = max(EMG1) - min(EMG1)
				# range2 = max(EMG2) - min(EMG2)
				maxEMG1 = max(abs(numpy.array(EMG1)))
				maxEMG2 = max(abs(numpy.array(EMG2)))
				# print str(maxEMG1) + " " + str(maxEMG2)
				# and maxEMG1 > 200 and maxEMG2 > 200
				if ((maxEMG1 > 35 or maxEMG2 > 35) and maxEMG1 > 30 and maxEMG2 > 30 and chunk.startTime - EMGOVBox.forwardPrevTime > 3):
					EMGOVBox.forwardPrevTime = chunk.startTime
					print "Open Mouth"
					## Do something to active voice assistant system
					
				elif (maxEMG2 > 50 and chunk.startTime > 10):
					EMGOVBox.count += 1
					# print str(maxEMG1) + " " + str(maxEMG2)
					if (EMGOVBox.count > 4 and EMGOVBox.keepState == 0):
						EMGOVBox.keepState = 1
						print "Chewing"
				elif (EMGOVBox.count != 0 and maxEMG2 < 50):
					EMGOVBox.count -= 0
					if EMGOVBox.count > 4:
						EMGOVBox.count = 0
						EMGOVBox.keepState = 0

			elif(type(self.input[0][chunkIndex]) == OVSignalEnd):
				print "end"
				self.output[0].append(self.input[0].pop())	 			

box = EMGOVBox()