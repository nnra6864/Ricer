import re

class Color:
    def __init__(self, name, color):
        self.name = name
        self.r, self.g, self.b, self.a = 0, 0, 0, 0
        self.r01, self.g01, self.b01, self.a01 = 0, 0, 0, 0
        self.rgba, self.rgba01 = [], []
        self.hexa = "", ""
        
        self.parse_color(color)

        self.color_variables = {
            'hex': self.hexa[:-2],
            'hexa': self.hexa,
            'hr': self.hexa[0:2],
            'hg': self.hexa[2:4],
            'hb': self.hexa[4:6],
            'ha': self.hexa[6:8],
            'rgb': self.rgba[:3],
            'rgba': self.rgba,
            'r': self.rgba[0],
            'g': self.rgba[1],
            'b': self.rgba[2],
            'a': self.rgba[3],
            'rgb01': self.rgba01[:3],
            'rgba01': self.rgba01,
            'r01': self.rgba01[0],
            'g01': self.rgba01[1],
            'b01': self.rgba01[2],
            'a01': self.rgba01[3]
        }

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
        from Config import Config
        color = color.strip().lstrip('#')
        if re.match(r'^([0-9a-fA-F]{6})$', color):
            color += "FF"
        if re.match(r'^([0-9a-fA-F]{8})$', color):
            self.hexa = color.upper()
            self.r, self.g, self.b, self.a = Color.hexa_to_rgba(color)
            self.r01, self.g01, self.b01, self.a01 = (round(x / 255, Config.rgba01_precision) for x in (self.r, self.g, self.b, self.a))
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
            self.rgba01 = tuple(round(float(val), Config.rgba01_precision) if '.' in val else round(int(val) / 255.0, Config.rgba01_precision) for val in vals)
            self.r, self.g, self.b, self.a = self.rgba
            self.r01, self.g01, self.b01, self.a01 = self.rgba01
            self.hexa = Color.rgba_to_hexa(self.rgba)
            return
        raise ValueError(f"Invalid color format: {color} for {self.name}")
    
    def format_color(self, format: str) -> str:
        pattern = re.compile(r'\b(' + '|'.join(re.escape(key) for key in self.color_variables.keys()) + r')\b')
        return pattern.sub(lambda match: str(self.color_variables[match.group(1)]), format)
