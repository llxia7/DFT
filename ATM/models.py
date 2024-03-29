from django.db import models

class Action_Map(models.Model):
	sub_flow			= models.CharField(max_length=30,unique=True)
	action				= models.CharField(max_length=20)
	instrument_model	= models.CharField(max_length=20)
	device				= models.ForeignKey('Device', on_delete=models.CASCADE)

	class Meta:
		ordering = ['instrument_model']

	def __str__(self):
		return self.sub_flow


class Test_Log(models.Model):
	log_name	= models.CharField(max_length=50,unique=True)
	test_date	= models.DateTimeField()
	device		= models.ForeignKey('Device', on_delete=models.CASCADE)
	stage		= models.CharField(max_length=20)
	save_date	= models.DateField()

	class Meta:
		ordering = ['test_date']
		
	def __str__(self):
		return self.log_name


class Device(models.Model):
	name	= models.CharField(max_length=30,unique=True)

	def __str__(self):
		return self.name
	

class Result_Detail(models.Model):
	log_name	= models.ForeignKey('Test_Log', on_delete=models.CASCADE)
	sub_flow	= models.ForeignKey('Action_Map', on_delete=models.CASCADE)
	RESULT_CHOICES = (
		('P', 'Pass'),
		('F', 'Fail'),
	)
	result		= models.CharField(max_length=2, choices=RESULT_CHOICES)

	class Meta:
		ordering = ['log_name']
	
	def __str__(self):
		return self.log_name.log_name + self.sub_flow.sub_flow

