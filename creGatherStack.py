#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# creGatherStack.py  (Madagascar Recipe)
#
# Purpose: CRE stacking recipe.
# 
# Important!: It should be called from a SConstruct 
#
# Site: https://www.geofisicando.com
# 
# Version 1.0
#
# Programmer: Rodolfo A. C. Neves (Dirack) 04/03/2020
#
# Email: rodolfo_profissional@hotmail.com
#
# License: GPL-3.0 <https://www.gnu.org/licenses/gpl-3.0.txt>.

'''
Madagascar recipe to CRE stacking

Define functions to generate the Zero-offset section using CRE stacking
'''

if __name__ == "__main__":
	print(__doc__)
	exit()

# Madagascar package
from rsf.proj import *

# Madagascar Recipes
from rsf.recipes.kimodel import multiLayerModelBuild
from rsf.recipes.kimodel import kirchhoffNewtonModeling
from rsf.recipes.pefInterpolation2 import pefInterpolation
from rsf.recipes.utils import arr2str
from rsf.recipes.utils import velplot

__author__="Rodolfo Dirack <rodolfo_profissional@hotmail.com>"
__version__="1.0"

def modeling(modelfile,
        dataCube,
        xmax,
        zmax,
        layers,
        velocities,
        nt,
        dt,
        ns,
        ds,
        nh,
        dh):
    '''

    This is a wrapper function to multiLayerModelBuild function that builds the layers velocity model
    and to the kirchhoffNewtonModeling that generates the seismic data cube applying the Kirchhoff
    modeling to the velocity model built

    :param modelfile: RSF filename, velocity model
    :param dataCube: RSF filename, seismic data cube
    :param xmax: interger, max x axis model distance
    :param zmax: interger, max z axis model depth
    :param layers: tuple array, points describing interfaces
    :param velocities: tuple, layers velocities in km/s
    :param nt: integer, number of time samples
    :param dt: float, time sampling
    :param ns: integer, number of CMP samples
    :param ds: float, CMP sampling
    :param nh: integer, number of offset samples
    :param dh: float, offset sampling
    '''
    multiLayerModelBuild(
        interfaces=modelfile+'-interfaces',
        dipsfile=modelfile+'-interfacesDip',
        modelfile=modelfile,
        xmax=xmax,
        zmax=zmax,
        layers=layers,
        velocities=velocities)

    kirchhoffNewtonModeling(
        reflectors=modelfile+'-interfaces',
        reflectorsDip=modelfile+'-interfacesDip',
        filename=dataCube,
        velocities=velocities,
        nt=nt,
        dt=dt,
        ns=ns,
        ds=ds,
        nh=nh,
        dh=dh)

def interpolation(dataCube,
        interpolated1,
        interpolated2,
        nm,
        dm,
        nt,
        dt,
        nhi,
        a1,
        a2,
        rect1,
        rect2):
    '''
    
    PEF interpolation to increase number of CMPs
    Interpolation is done twice, so interpolated1 is the intermediate interpolated
    data cube that is interpolated again to generate interpolated2 data cube

    This is just a wrapper function to apply the pefInterpolation function two times
    and increase the number of CMPs in seismic data cube by four times

    :param dataCube: RSF filename, seismic data cube
    :param interpolated1: RSF filename, intermediate interpolated data cube
    :param interpolated2: RSF filename, interpolated data cube
    :param nm: int, Number of CMPs in seismic data cube
    :param dm: float, CMPs sampling in seismic data cube
    :param nt: int, Number of time samples in seismic data cube
    :param dt: float, time sampling in seismic data cube
    :param nhi: int, Number of offsets to interpolated
    :param a1: integer, Number of PEF coeficients in time axis
    :param a2: integer, Number of PEF coeficients in space axis
    :param rect1: integer, Smooth radius in time
    :param rect2: integer, Smooth radius in space
    '''
    pefInterpolation(dataCube=dataCube,
    interpolated=interpolated1,
    nm=nm,
    dm=dm,
    nt=nt,
    dt=dt,
    nhi=nhi,
    a1=a1,
    a2=a2,
    rect1=rect1,
    rect2=rect2)

    pefInterpolation(dataCube=interpolated1,
    interpolated=interpolated2,
    nm=2*nm,
    dm=dm/2.0,
    nt=nt,
    dt=dt,
    nhi=nhi,
    a1=a1,
    a2=a2,
    rect1=rect1,
    rect2=rect2)

def vfsa(parametersCube,
        interpolatedDataCube,
        nm0,
        om0,
        dm0,
        nt0,
        ot0,
        dt0,
        v0,
        repeat,
        itmax,
        rnmin,
        rnmax,
        rnipmin,
        rnipmax,
        betamin,
        betamax,
        half='y',
        verb='y'):
    '''
    
    Very Fast Simulated Annealing (VFSA) global optimization of zero-offset
    CRS parameters (RN, RNIP, BETA)

    :param parametersCube: RSF filename, parameters cube (RN,RNIP,BETA)
    :param interpolatedDataCube: RSF filename, interpolated seismic data cube
    :param nm0: int, number of m0s (CMPs in stacked section)
    :param om0: float, m0s axis origin
    :param dm0: float, m0s sampling
    :param nt0: int, number of t0s (t0s in stacked section)
    :param ot0: float, t0s axis origin
    :param dt0: float, t0s sampling
    :param v0: float, Near surface velocity
    :param repeat: int, number of VFSA repetitions
    :param itmax: int, number of VFSA iterations each repetition
    :param rnmin: float, RN minimum
    :param rnmax: float, RN maximum
    :param rnipmin: float, RNIP minimum
    :param rnipmax: float, RNIP maximum
    :param betamin: float, BETA minimum
    :param betamax: float, BETA maximum
    :param half: str, (y/n) seismic data cube in half-offset coordinates
    :param verb: str, (y/n) verbose parameter
    '''
    Flow(parametersCube,interpolatedDataCube,
    '''
    vfsacrsnh nm0=%d om0=%g dm0=%g nt0=%d ot0=%g dt0=%g v0=%g repeat=%d itmax=%d verb=%s
    rnmin=%g rnmax=%g rnipmin=%g rnipmax=%g betamin=%g betamax=%g half=%s
    '''%(nm0,om0,dm0,nt0,ot0,dt0,v0,repeat,itmax,verb,rnmin,rnmax,rnipmin,rnipmax,betamin,betamax,half))


def stack(stackedSection,
        interpolatedDataCube,
        parametersCube,
        nm0,
        om0,
        dm0,
        nt0,
        ot0,
        dt0,
        v0,
        aperture):
    '''

    CRE stacking

    :out stackedSection: RSF file, stacked section
    :param interpolatedDataCube: RSF file, interpolated seismic data cube
    :param parametersCube: RSF file, RN, RNIP and BETA
    :param nm0: int, number of m0s
    :param om0: float, m0s axis origin
    :param dm0: float, m0s sampling
    :param nt0: int, number of t0s
    :param ot0: float, t0s axis origin
    :param dt0: float, t0s sampling
    :param v0: float, near surface velocity
    :param aperture: int, number of offsets to stack
    '''
    creTrajectories = interpolatedDataCube+'-creTrajectories'
    cregathers = interpolatedDataCube+'-cregathers'
    mhCoordinates = interpolatedDataCube+'-mhCoordinates'
    cretimecurves = interpolatedDataCube+'-cretimecurves'

    Flow(creTrajectories,[interpolatedDataCube,parametersCube],
        '''
        cretrajec param=${SOURCES[1]} nm0=%d om0=%g dm0=%g nt0=%d ot0=%g dt0=%g verb=y
        '''%(nm0,om0,dm0,nt0,ot0,dt0))

    Flow([cregathers,mhCoordinates],[interpolatedDataCube,creTrajectories],
        '''
        getcregather cremh=${SOURCES[1]} m=${TARGETS[1]} aperture=%d nm0=%g nt0=%g |
        put label1=Time unit1=s label2=Offset unit2=Km label3=t0 unit3=s
        label4=m0 unit4=Km n3=%d d3=%g o3=%g n4=%d d4=%g o4=%g
        ''' % (aperture,nm0,nt0,nt0,dt0,ot0,nm0,dm0,om0))

    Flow(cretimecurves,[mhCoordinates,parametersCube],
        '''
        getcretimecurve param=${SOURCES[1]} nm0=%d om0=%g dm0=%g nt0=%d ot0=%g dt0=%g verb=y v0=%g |
        put label1=Offset unit1=Km label2=t0 unit2=s label3=m0 unit3=Km
        n2=%d d2=%g o2=%g n3=%d d3=%g o3=%g
        '''%(nm0,om0,dm0,nt0,ot0,dt0,v0,nt0,dt0,ot0,nm0,dm0,om0))

    Flow(stackedSection,[cregathers,cretimecurves],
        '''
        crestack aperture=%d verb=y timeCurves=${SOURCES[1]} |
        put label1=t0 unit1=s label2=m0 unit2=Km
        ''' %(aperture))

