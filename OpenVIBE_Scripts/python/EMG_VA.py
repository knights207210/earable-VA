import numpy
from selenium import webdriver
#https://sites.google.com/a/chromium.org/chromedriver/getting-started
from selenium.webdriver.common.keys import Keys


# open browser first
# path needs to be edited
driver = webdriver.Chrome("/Users/hanxu/Downloads/chromedriver")
#driver.fullscreen_window()
driver.get('https://developer.amazon.com/alexa/console/ask/test/amzn1.ask.skill.84d0b864-bcf0-4af5-a99b-abdc3b5b384d/development/en_US/')

username = "wangyichen5151@gmail.com"
password = "woailianlian"

elem_email=driver.find_element_by_id("ap_email")
elem_email.send_keys(username)
elem_ps = driver.find_element_by_id("ap_password")
elem_ps.send_keys(password)
elem_si = driver.find_element_by_id("signInSubmit")
elem_si.click()


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

					command = "tell earablexuhan about to open the mouth"
					elem = driver.find_element_by_class_name("askt-utterance__input")
                	elem.send_keys(command)
                	elem.send_keys(Keys.ENTER)
					


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