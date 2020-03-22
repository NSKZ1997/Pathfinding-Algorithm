import math

class Vector:
    def __init__(self, arguments):
        self.arguments = arguments
       
    def __add__(vector1, vector2):
        if Vector.check_if_equal(vector1, vector2):
            empty_list = []
            for i in range(len(vector1)):
                empty_list.append(vector1[i] + vector2[i])
            return Vector(empty_list)
        
    def __sub__(vector1, vector2):
        if Vector.check_if_equal(vector1, vector2):
            empty_list = []
            for i in range(len(vector1)):
                empty_list.append(vector1[i] - vector2[i])
            return Vector(empty_list)
    
    def __mul__(vector, number):
        for i in range(len(vector.arguments)):
            vector[i] *= number
        return vector
            
    def __truediv__(vector, number):
        for i in range(len(vector.arguments)):
            vector[i] /= number
        return vector
     
    #I don't know why you'd want to do this but the option is there. 
    @classmethod
    def multiply(cls, vector1, vector2):
        if Vector.check_if_equal(vector1, vector2):
            empty_list = []
            for i in range(len(vector1)):
                empty_list.append(vector1[i] * vector2[i])
            return cls(empty_list)
    
    @classmethod
    def divide(cls, vector1, vector2):
        if Vector.check_if_equal(vector1, vector2):
            empty_list = []
            for i in range(len(vector1)):
                empty_list.append(vector1[i] / vector2[i])
            return cls(empty_list)
        
    def __len__(self):
        return len(self.arguments)
    
    def __repr__(self):
        return 'A vector with elements: ' + str(self.arguments)
    
    def __iter__(self):
        yield from self.arguments
    
    def __getitem__(self, i):
        return self.arguments[i]
    
    def __setitem__(self, i, value):
        self.arguments[i] = value
    
    def __eq__(vector1, vector2):
        if Vector.check_if_equal(vector1, vector2):
            for i in range(len(vector1)):
                if vector1[i] != vector2[i]:
                    return False
            return True
        
    def append_elements(self, *elements):
        for element in elements:
            self.arguments.append(element)
            
    def length(self):
        result = 0
        for element in self:
            result += element ** 2
        result = result ** 0.5
        return result
    
    @classmethod
    def dot_product(self, vector1, vector2):
        if Vector.check_if_equal(vector1, vector2):
            sum = 0
            for i in range(len(vector1)):
                sum += vector1[i] * vector2[i]
            return sum
    
    @classmethod
    def angle(cls, vector1, vector2):
        return math.acos(Vector.dot_product(vector1, vector2)/(vector1.length() * vector2.length()))
    
    @classmethod
    def angle_degrees(cls, vector1, vector2):
        return math.acos(Vector.dot_product(vector1, vector2)/(vector1.length() * vector2.length())) * 90/(math.pi/2)
    
    def degrees(self):
        elements = []
        for i in range(len(self.arguments) - 1):
            elements.append(0)
        elements.append(1)     
        return Vector.angle_degrees(self, Vector(elements))
    
    @classmethod
    def check_if_equal(cls, vector1, vector2):
        if len(vector1) != len(vector2):
            raise Exception("Error. Vectors must be of same length. (Vector 1 length: {}), (Vector 2 length: {})".format(len(vector1.arguments), len(vector2.arguments)))
        return True
    
    def norm(self):
        length = self.length()
        for i in range(len(self)):
            self.arguments[i] /= length
        return self.arguments
    
    def move(self, direction, amount):
        if Vector.check_if_equal(self, direction):
            add_amount = Vector(direction) * amount
            for i in range(len(self)):
                self.arguments[i] += add_amount[i]
            return vector
    
    @classmethod
    def cross_product(cls, vector1, vector2):
        pass
    
   
def is_between(number, boundary1, boundary2):
    boundary1, boundary2 = min(boundary1, boundary2), max(boundary1, boundary2)
    if number >= boundary1 and number <= boundary2:
        return True
    return False

vector = Vector([4, 5])
vector.move([1, 1], 5)
print(vector)