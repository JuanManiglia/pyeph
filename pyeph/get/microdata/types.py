# -*- coding: utf-8 -*-
from datetime import date

class BaseType(object):

	VALUES = ['individual','hogar']

	def __get__(self, obj, *args):
		return self.value

	def __set__(self, obj, value):
		if not (isinstance(value,str) and value in self.VALUES):
			raise ValueError("Por favor ingresa un tipo de base valido: " + ", ".join(self.VALUES))
		self.value = value

class Frequency(object):

	VALUES = {
        'trimestre': 4,
        'onda': 2
    }

	def __get__(self, obj, *args):
		return self.value

	def __set__(self, obj, value):
		if not (isinstance(value,str) and value in self.VALUES):
			raise ValueError("Por favor ingresa un tipo de base valido: " + ", ".join(self.VALUES.keys()))
		self.value = value

class Period(object):

	VALUES = [1,2,3,4]

	def __get__(self, obj, *args):
		return self.value

	def __set__(self, obj, value):
		if not (
			(isinstance(value,int) and value in self.VALUES) or
			value is None
		):
			raise ValueError("Por favor ingresa un numero de trimeste valido: " + ",".join(map(str, self.VALUES)))
		self.value = value

class Year(object):
	def __get__(self, obj, *args):
		return self.value

	def __set__(self, obj, value):
		current_year = date.today().year
		if not (isinstance(value,int) and value <= current_year):
			raise ValueError("El año debe ser menor o igual a {}.".format(current_year))
		self.value = value

