import re

class Color:
    def __init__(self, name, color):
        self.name = name
        self.r, self.g, self.b, self.a = None, None, None, None
        self.r01, self.g01, self.b01, self.a01 = None, None, None, None
        self.rgba, self.rgba01 = None, None
        self.hexa = None
        
        self.parse_color(color)

    @staticmethod
    def hexa_to_rgba(hexa):
        hexa = hexa.lstrip('#')
        
        if len(hexa) not in (6, 8) or not all(c in '0123456789ABCDEFabcdef' for c in hexa):
            raise ValueError(f"Invalid HEXA value: {hexa}")
        if len(hexa) == 6:
            hexa += "FF"
        
        return tuple(int(hexa[i:i+2], 16) for i in (0, 2, 4, 6))

    @staticmethod
    def rgba_to_hexa(rgba):
        if len(rgba) == 3:
            r, g, b = rgba
            a = 255
        elif len(rgba) == 4:
            r, g, b, a = rgba
        else:
            raise ValueError(f"Invalid RGBA value: {rgba}")
        return f"{r:02X}{g:02X}{b:02X}{a:02X}"

    def parse_color(self, color):
        color = color.strip().lstrip('#')
        if re.match(r'^([0-9a-fA-F]{6})$', color):
            color += "FF"
        if re.match(r'^([0-9a-fA-F]{8})$', color):
            self.hexa = color.upper()
            self.r, self.g, self.b, self.a = Color.hexa_to_rgba(color)
            self.r01, self.g01, self.b01, self.a01 = (x / 255 for x in (self.r, self.g, self.b, self.a))
            self.rgba = (self.r, self.g, self.b, self.a)
            self.rgba01 = (self.r01, self.g01, self.b01, self.a01)
            return
            
        match = re.search(r'rgb\(\s*([\d\.]+(?:\s*,\s*[\d\.]+)*)\s*\)', color)
        if match:
            vals = re.findall(r'[\d\.]+', match.group(1))
            ln = len(vals)
            
            if ln == 3:
                vals.append("255")
            if ln != 4:
                raise ValueError(f"Invalid number of values in RGB format: {color}")
            self.rgba = tuple(int(float(val) * 255 if '.' in val else val) for val in vals)
            self.rgba01 = tuple(float(val) if '.' in val else int(val) / 255.0 for val in vals)
            self.r, self.g, self.b, self.a = self.rgba
            self.r01, self.g01, self.b01, self.a01 = self.rgba01
            self.hexa = Color.rgba_to_hexa(self.rgba)
            return
        raise ValueError(f"Invalid color format: {color} for {self.name}")

