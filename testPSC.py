import PitchSetClasses

psc = PitchSetClasses.pitchSetClass()

prime = '012358'
name = '9-2'
print('By Prime: ', psc.getByPrime(prime))
print('By Name: ', psc.getByName(name))
