import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.dates as md
import modules.database as db

class GraphTraffic:

	def __init__(self):
		self.db = db.DB_VPS()

	def genGraph(self,interface):

		self.filenames = []

		for intdev in interface:

			self.filename = "static/graphs/{}".format(intdev[1])
			self.interface = "tap{}".format(intdev[1])
			self.filenames.append(self.filename)
			
			row = []
			row = self.db.getTrafficData(self.interface)

			if (len(row) > 0):

				self.opackets = []
				self.ipackets = []
				self.timestamp = []

				#count = 0

				for line in row:

					"""if count == 0:
						ipkgs = line[0]
						opkts = line[1]
					else:
						ipkgs = line[0] - ipkgs
						opkts = line[1] - opkts"""

					ipkgs = line[0]/1024
					opkts = line[1]/1024
						
					tmestmp = dt.datetime.fromtimestamp(line[2])

					self.opackets.append(opkts)
					self.ipackets.append(ipkgs)
					self.timestamp.append(tmestmp)

					#count = count + 1

				# plot
				plt.subplots_adjust(bottom=0.2)

				plt.xticks( rotation=25 )
				ax=plt.gca()
				xfmt = md.DateFormatter('%H:%M')
				ax.xaxis.set_major_formatter(xfmt)


				plt.plot(self.timestamp,self.ipackets)
				plt.plot(self.timestamp,self.opackets)
				# beautify the x-labels
				plt.gcf().autofmt_xdate()
				plt.grid(True)
				plt.xlabel(self.interface, fontsize=14, color='red')
				plt.legend(['In', 'Out'], loc='best')
				plt.savefig(self.filename)
				plt.gcf().clear()


			#plt.show()
		

		return self.filenames