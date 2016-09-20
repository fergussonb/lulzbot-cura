__author__ = "Berkeley Fergusson"


"""Class to estimate the average energy that will be needed to run a print job"""

from Cura.util import profile


class energy(object):
    def __init__(self, time):
        self.time = 0.0 + time
        self.time /= 60
        startE = 0
        material = "%s" % profile.getProfileSetting('simpleModeMaterial')
        if 'PLA' in material:
            startE = "%s" % profile.getMachineSetting('machine_startup_energy_PLA')
        elif 'ABS' in material:
            startE = "%s" % profile.getMachineSetting('machine_startup_energy_ABS')
        elif 'HIPS' in material:
            startE = "%s" % profile.getMachineSetting('machine_startup_energy_HIPS')
        elif 't-glase' in material:
            startE = "%s" % profile.getMachineSetting('machine_startup_energy_PETT')
        elif 'Nylon' in material:
            startE = "%s" % profile.getMachineSetting('machine_startup_energy_Nylon')
        else:
            startE = "%s" % profile.getMachineSetting('machine_startup_energy_Other')
        self.startupEnergy = int(startE)
        averageE = 0
        if 'PLA' in material:
            averageE = "%s" % profile.getMachineSetting('machine_run_energy_PLA')
        elif 'ABS' in material:
            averageE = "%s" % profile.getMachineSetting('machine_run_energy_ABS')
        elif 'HIPS' in material:
            averageE = "%s" % profile.getMachineSetting('machine_run_energy_HIPS')
        elif 't-glase' in material:
            averageE = "%s" % profile.getMachineSetting('machine_run_energy_PETT')
        elif 'Nylon' in material:
            averageE = "%s" % profile.getMachineSetting('machine_run_energy_Nylon')
        else:
            averageE = "%s" % profile.getMachineSetting('machine_startup_energy_Other')
        self.averageEnergy = int(averageE)

    def getRunEnergy(self):
        totalE = 0.0
        totalE += self.startupEnergy
        totalE += self.averageEnergy * self.time
        return totalE



#e = energy(5)
#print e.time
