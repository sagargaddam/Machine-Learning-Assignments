import numpy as np
import pandas as pd
import sys

# Defining a generalized regression class
class Regression:

	def __init__(self,pd_x,pd_y,normalize_x=True,normalize_y=False):
		self.dataframe_x=pd_x
		self.dataframe_y=pd_y
		temp_x=self.dataframe_x.values
		temp_y=self.dataframe_y.values

		#whether or not to normalize x
		if(normalize_x):
			self.x_mu=self.getMean(temp_x)
			self.x_sigma=self.getStd(temp_x)
			temp_x=self.normalize(temp_x,self.x_mu,self.x_sigma)

		#whether or not to normalize y
		if(normalize_y):
			self.y_mu=self.getMean(temp_y)
			self.y_sigma=self.getStd(temp_y)
			temp_y=self.normalize(temp_y,self.y_mu,self.y_sigma)

		self.x=self.append_1(temp_x)
		self.y=temp_y
		[instances,parameters]=self.x.shape
		self.theta=np.zeros((parameters,1))
		self.epoch=0
		self.train_steps=0

	# Appending 1 to train_samples

	def append_1(self,x):
		[instances,parameters]=x.shape
		ones_column=np.ones((instances,1))
		return np.concatenate((ones_column,x),axis=1)

	def getMean(self,x):
		return np.mean(x,axis=0)

	def getStd(self,x):
		return np.std(x,axis=0)

	def normalize(self,x,mu,sigma):
		return (x-mu)/sigma

	def evaluate(self,x):
		return np.matmul(x,self.theta)

	def getLoss(self,x,y):
		aux_diff=self.evaluate(x)-y
		temp_loss=np.transpose(aux_diff)
		return 0.5*(np.matmul(temp_loss,aux_diff))

	def getGradient(self,x,y):
		aux_loss=(y-self.evaluate(x))
		aux_grad=np.matmul(np.transpose(x),aux_loss)
		return (-1*aux_grad)


	def train(self,learning_rate=0.01,epsilon=0.1,batch_mode=False,batch_size=1000,log_every_epoch=100):

		[instances,parameters]=self.x.shape
		[_,y_shape]=self.y.shape

		if(batch_mode==False):
			batch_size=instances

		prev_loss=self.getLoss(self.x,self.y)
		Trained=False

		while(Trained==False):

			cur_trained=0
			self.epoch=self.epoch+1

			while(cur_trained<instances):
				
				self.train_steps=self.train_steps+1
				upper_limit=min(cur_trained+batch_size,instances)

				train_x=self.x[cur_trained:upper_limit,0:parameters]
				train_y=self.y[cur_trained:upper_limit,0:y_shape]
				cur_trained=upper_limit

				gradient=self.getGradient(train_x,train_y)
				self.theta=(self.theta-learning_rate*gradient)
				current_loss=self.getLoss(train_x,train_y)

				if(abs(current_loss-prev_loss)<epsilon):
					Trained=True
					break
				prev_loss=current_loss

			if(self.epoch%log_every_epoch==0):
				print ("epoch: ",self.epoch," ",self.getLoss(self.x,self.y))
			# if(self.epoch==100):
			# 	break


def main(path_x,path_y):

	temp_x=pd.read_csv(path_x,header=None,sep=',')
	temp_y=pd.read_csv(path_y,header=None,sep=',')

	myReg=Regression(pd_x=temp_x,pd_y=temp_y,normalize_x=True)
	# print (temp_x.values.shape)
	# print (temp_y.values.shape)
	# print (temp_x.values)
	# print(temp_y.values)


	# print (myReg.x.shape)
	# print (myReg.y.shape)
	myReg.train(log_every_epoch=50,learning_rate=0.005,epsilon=0.000001)
	print (myReg.train_steps)
	print (myReg.epoch)
	print (myReg.getLoss(myReg.x,myReg.y))
	

if __name__=="__main__":

	main(sys.argv[1],sys.argv[2])