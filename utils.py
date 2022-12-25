#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# utils.py  (Madagascar Recipe)
#
# Purpose: Utility functions.
# 
# Important!: It should be called from a SConstruct 
#
# Site: http://www.geofisicando.com
# 
# Version 1.0
#
# Programer: Rodolfo A. C. Neves (Dirack) 24/12/2022
#
# Email: rodolfo_profissional@hotmail.com
#
# License: GPL-3.0 <https://www.gnu.org/licenses/gpl-3.0.txt>.

'''
Madagascar recipe with utility functions
'''

if __name__ == "__main__":
	print(__doc__)
	exit()

__author__="Rodolfo Dirack <rodolfo_profissional@hotmail.com>"
__version__="1.0"

def arr2str(array,sep=' '):
	'''
	
	Convert a tuple into a comma separeted string
	
	:param array: tuple to be converted
	'''
	return sep.join(map(str,array))

def velplot(title,barunit="km/s",bias=1.0):
    '''

    Return a string for velocity model plot with Result
    scons function

    Usage example: Result(rsfmodel,velplot("Model 4","m/s","1.5"))

    :param title: Velocity model title
    :param barunit: Scalebar unit
    :param bias: Bias parameter for sfgrey
    '''
    return '''
    grey color=j scalebar=y barlabel=Velocity barunit=%s
    barreverse=y title="%s" allpos=y bias=%g
    ''' % (barunit,title,bias)

def plotStackedSection(title,label1="t0",unit1="s",label2="m0",unit2="km"):
    '''

    Return a string for stacked section plot with Result scons function

    Usage example: Result(rsfsection,plotStackedSection("Section"))

    :param title: Stacked section title
    :param label1: Label axis 1
    :param unit1: Unit axis 1
    :param label2: Label axis 2
    :param unit2: Unit axis 2
    '''
    return '''
    grey title="%s" label1="%s" unit1="%s" label2="%s" unit2="%s"
    ''' % (title,label1,unit1,label2,unit2)
