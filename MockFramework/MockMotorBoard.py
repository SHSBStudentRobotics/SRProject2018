
#A Mock motor board that prints out every change.
class MockMotorBoardPrinter:
    def __init__(self):
        self._m0 = 0
        self._m1 = 0

    def setM0(self , value):
        print("m0 Changed to: " + str(value))
        self._m0 = value

    def getM0(self, value):
        return self._m0

    def setM1(self , value):
        print("m1 Changed to: " + str(value))
        self._m1 = value

    def getM1(self, value):
        return self._m1

    m0 = property(getM0,setM0)
    m1 = property(getM1,setM1)

#A Mock motor board that simply stores the values, for silent testing.
class MockMotorBoard:
    m0 = 0
    m1 = 0