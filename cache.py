from field import Field

class Cache:

    def __init__(self, field):
        self.queue = []
        self.field = field

    def calculate_one_tick(self):
        print("Cache has {} entrys,".format(len(self.queue)))
        if self.queue == []:
            f = Field(copy_field=self.field)
            f.update()
            self.queue.append(f)
        elif len(self.queue) < 5:
            f = Field(copy_field=self.queue[-1])
            f.update()
            self.queue.append(f)
    
    def get_next(self, dirty=False):
        if dirty:
            self.queue = []
            self.field.update()
            return self.field
        
        if self.queue == []:
            return self.get_next(dirty=True)

        self.field = self.queue.pop(0)
        return self.field
