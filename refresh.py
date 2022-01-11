class Refresh_Drawn():
    def __init__(self, rate):
        self.rate = rate
        self.current = 0

    def set_draw_function(self, function):
        self.function = function
    
    def set_refresh_rate(self, rate):
        self.rate = rate

    def refresh(self):
        self.current += 1
        if self.current % self.rate != 0:
            return
        self.function()