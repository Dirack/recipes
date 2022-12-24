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

# Selfdoc string
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
    TODO
    '''
    return '''
    grey color=j scalebar=y barlabel=Velocity barunit=%s
    barreverse=y title="%s" allpos=y bias=%g
    ''' % (barunit,title,bias)

def plotStackedSection(title,label1="t0",unit1="s",label2="m0",unit2="km"):
    '''
    TODO
    '''
    return '''
    grey title="%s" label1="%s" unit1="%s" label2="%s" unit2="%s"
    ''' % (title,label1,unit1,label2,unit2)
