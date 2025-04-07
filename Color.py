import re
from colorsys import rgb_to_hsv, hsv_to_rgb

class Color:
    def __init__(self, name, color):
        self.name = name
        self.r, self.g, self.b, self.a = 0, 0, 0, 0
        self.r01, self.g01, self.b01, self.a01 = 0, 0, 0, 0
        self.rgba, self.rgba01 = [], []
        self.hexa = ""
        self.color_variables = {}
        self.load_color(color)

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

    def load_color(self, color: str):
        from Config import Config
        
        # Split the color string into base color and modifiers
        parts = re.split(r'\.(?![^()]*\))', color)
        base_color = parts[0]
        modifiers = parts[1:]
    
        # Handle color variables (starting with $)
        if base_color.startswith('$'):
            col_key = base_color[1:]
            if col_key in Config.colors:
                base_color = Config.colors[col_key].hexa
            else:
                raise ValueError(f"Undefined color variable: {base_color} for {self.name}")
    
        # Parse the base color
        base_color = base_color.strip().lstrip('#')
        if re.match(r'^([0-9a-fA-F]{6})$', base_color):
            base_color += "FF"
        if re.match(r'^([0-9a-fA-F]{8})$', base_color):
            self.hexa = base_color.upper()
            self.rgba = Color.hexa_to_rgba(base_color)
        else:
            match = re.search(r'rgba?\(\s*([\d\.]+(?:\s*,\s*[\d\.]+)*)\s*\)', base_color)
            if match:
                vals = re.findall(r'[\d\.]+', match.group(1))
                ln = len(vals)
                if ln == 3:
                    vals.append("255")
                if ln != 4:
                    raise ValueError(f"Invalid number of values in RGB(A) format: {base_color}")
                self.rgba = tuple(int(float(val) * 255 if '.' in val else val) for val in vals)
                self.hexa = Color.rgba_to_hexa(self.rgba)
            else:
                raise ValueError(f"Invalid color format: {base_color} for {self.name}")
    
        self.r, self.g, self.b, self.a = self.rgba
        self.rgba01 = tuple(round(x / 255, Config.rgba01_precision) for x in self.rgba)
        self.r01, self.g01, self.b01, self.a01 = self.rgba01
    
        # Apply modifiers
        # Apply modifiers
        if modifiers:  # Only apply HSV modifications if there are modifiers
            h, s, v = rgb_to_hsv(self.r01, self.g01, self.b01)

            def apply_mod(mod):
                nonlocal h, s, v
                match = re.match(r'([hsvHSV])([+-]\d+)', mod)
                if match:
                    component, value = match.groups()
                    value = int(value)
                    if component.lower() == 'h':
                        h = (h + value / 360) % 1
                    elif component.lower() == 's':
                        s = max(0, min(1, s + value / 100))
                    elif component.lower() == 'v':
                        v = max(0, min(1, v + value / 100))
                else:
                    raise ValueError(f"Invalid modifier format: {mod} for {self.name}")

            for mod in modifiers:
                if mod.startswith('$'):
                    # Handle variable modifiers
                    var_key = mod[1:]
                    if var_key in Config.values:
                        var_value = Config.values[var_key]
                        # Check if the variable contains multiple modifiers
                        if '.' in var_value:
                            for sub_mod in var_value.split('.'):
                                apply_mod(sub_mod)
                        else:
                            apply_mod(var_value)
                    else:
                        raise ValueError(f"Undefined value variable: {mod} for {self.name}")
                else:
                    apply_mod(mod)

            # Convert back to RGB
            r, g, b = hsv_to_rgb(h, s, v)
            self.r01, self.g01, self.b01 = r, g, b
            self.r, self.g, self.b = int(r * 255), int(g * 255), int(b * 255)
            self.rgba = (self.r, self.g, self.b, self.a)
            self.rgba01 = (self.r01, self.g01, self.b01, self.a01)
            self.hexa = Color.rgba_to_hexa(self.rgba)

        self.update_color_variables()

    def update_color_variables(self):
        self.color_variables.update({
            'hex': self.hexa[:-2],
            'hexa': self.hexa,
            'hr': self.hexa[0:2],
            'hg': self.hexa[2:4],
            'hb': self.hexa[4:6],
            'ha': self.hexa[6:8],
            'rgb': ', '.join(map(str, self.rgba[:3])),
            'rgba': ', '.join(map(str, self.rgba)),
            'r': self.rgba[0],
            'g': self.rgba[1],
            'b': self.rgba[2],
            'a': self.rgba[3],
            'rgb01': ', '.join(map(str, self.rgba01[:3])),
            'rgba01': ', '.join(map(str, self.rgba01)),
            'r01': self.rgba01[0],
            'g01': self.rgba01[1],
            'b01': self.rgba01[2],
            'a01': self.rgba01[3]
        })

    def format_color(self, format: str) -> str:
        pattern = re.compile(r'\b(' + '|'.join(re.escape(key) for key in self.color_variables.keys()) + r')\b')
        return pattern.sub(lambda match: str(self.color_variables[match.group(1)]), format)
