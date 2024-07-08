<p align="center">
  <img src="https://i.imgur.com/1RYLZhE.png" alt="Ricer">
</p>

# Table Of Contents
- [Table Of Contents](#Table-Of-Contents)
- [Ricer](#Ricer)
- [Dependencies](#Dependencies)
- [Installation](#Installation)
- [Ricing](#Ricing)
    - [Config](#Config)
        - [Structure](#Structure)
        - [Multiple Rices](#Multiple-Rices)
        - [Settings](#Settings)
            - [Global](#Global)
            - [Values](#Values)
            - [Colors](#Colors)
            - [Files](#Files)
    - [Templates](#Templates)
        - [Keywords](#Keywords)
    - [Color Format](#Color-Format)
- [Links](#Links)

# Ricer
Ricer is a tool that aims to make the process of ricing easy.
It uses a single config file per rice with as many templates as needed.
Config is written in [TOML](https://toml.io/en/), and used to define all values, colors and files.
Templates are basically configuration files(e.g. alacritty.toml) which contain certain keywords that Ricer looks for and replaces.

# Dependencies
- ### [Colorama](https://pypi.org/project/colorama/)
- ### [Requests](https://pypi.org/project/requests/)
- ### [TOML](https://pypi.org/project/toml/)

# Installation
- Install all [dependencies](#Dependencies)
- Clone Ricer to a destination of your choice by running `git clone https://github.com/nnra6864/Ricer`

# Ricing
## [Config]
Ricer offers very powerful and extensive configuration using a single TOML file.
By default, Ricer looks for a config file at its default location, `~/.config/Ricer/`, called Config.toml.
In case it doesn't exist, Ricer will create needed directories and config file.<br/>
[Example Config](https://github.com/nnra6864/Ricer/blob/master/Config.toml)

### Structure
Every config consists of 3 key parts:
1. **Values** - All the basic values such as *int*, *bool*, *string* etc.
2. **Colors** - All the colors that can be defined in almost any way, *hex*, *rgb*, *rgb01* etc.
3. **Files** - All the template files Ricer will go through with target config files and formats.

### Multiple Rices
Intended way of managing multiple rices is having a separate config file for each rice.
They should all be placed in the Ricer config directory mentioned earlier in [Structure](#Structure).
Each config should have the same set of **Values** and **Colors**, while **Files** are optional.
To make the Ricer use a specific config file, you should pass it's path as an argument, e.g. `~/.config/Ricer/Nord.toml`

### Settings
#### [Global]
**Following settings should not be placed under a table.**
- **`alias`** - **`string`** - **`default: "ricer"`**, A word that Ricer looks for in template files.
- **`default_color_format`** - **`string`** - **`default: "hex"`**, Default color format that will be used for colors across all configs *(gets overridden by per file format)*.
- **`rgba01_precision`** - **`int`** - **`default: 2`**, Number of decimals Ricer will use when writing rgba01 values.
- **`replace_files`** - **`bool`** - **`default: false`**, If `true`, old config files will be replaced by new ones, if `false`, a backup of old config files will be created, called `config_name.backup`, before replacing them.
- **`create_example`** - **`bool`** - **`default: true`**, If `true`, an example template will be created in `config_dir/Files` when it's generated.
- **`color_log_format`** - **`string`**, A format that colors will be logged in during ricing *(string interpolation can be used to print the following properties: {name}, {hexa}, {rgba}, {rgba01})*.
- **`file_log_format`** - **`string`**, A format that files will be logged in during ricing *(string interpolation can be used to print the following properties: {name}, {path}, {path}, {target_path}, {format})*.
- **`space_colors`** - **`bool`** - **`default: false`**, Whether there is a space between colors when printing them
- **`space_files`** - **`bool`** - **`default: true`**, Whether there is a space between files when printing them

#### [Values]
**Values** is a table of variables to be used in your config files.
Any type supported by TOML should work.<br/>
Value examples:
- `bg = "Background.png"`
- `font_size = 13`
- `animate = false`

#### [Colors]
**Colors** is a table consisting of all the colors used in ricing.
Unlike Values, Colors are parsed in a specific way, allowing for the use of their properties.
This means that you can define a color, for example, HEX(`background = "2e3440")`, and then use it's RGB value when ricing.<br/>
All the following color definitions are valid:
- `col = "2e3440"` - HEX
- `col = "#2e3440"` - #HEX
- `col = "2e3440ff"` - HEXA
- `col = "#2e3440ff"` - #HEXA
- `col = "rgb(100, 255, 25)"` - RGB
- `col = "rgb(100, 255, 25, 255)"` - RGBA
- `col = "rgb(0.5, 1.0, 0.75)"` - RGB01
- `col = "rgb(0.5, 0.25, 0.75, 1.0)"` - RGBA01
- `col = "rgb(100, 1.0, 25)"` - RGBA+RGBA01
- `col = "rgb(0.5, 25, 1.0, 125)"` - RGBA+RGBA01

*To use the RGBA01 range, channel value has to be a float(even if it's one), e.g. `1.0`*
*If alpha channel isn't explicitly defined, it defaults to FF/255/1.0*

#### [Files]
**Files** table is used to define templates used in the ricing, their corresponding configs, and optionally color formats.
Files can be defined as:
- `template_name = "config_path"`
- `template_name = [ "config_path" ]`
- `template_name = [ "config_path", "color_format" ]`

Explanation:
- `template_name` has to be the exact same as the name of a template file located in `config_dir/Files/` with the option to exclude the extension.
Excluding the extension is recommended only if there is a single file with that name to avoid weird behaviour.
- `config_path` must point to the config file being replaced by a riced template, e.g. `~/.config/alacritty.toml`.
- `color_format` is a string that overrides the [`default_color_format`](#Global).

## [Templates]
**Templates** are copies of your config files containing certain keywords that Ricer looks for.
All templates must be located in the `config_dir/Files/` directory and preferrably have different names *(for ease of use)*.
When Ricer is started, it goes through all defined template files, copies their contents, replaces placeholders and copies the updated contents to their destination configs.

### Keywords
Ricer looks the alias, by default set to `ricer`, followed by the type - `val`/`col`, and a name, e.g. `background`.<br/>
Valid ways to access properties:
- `ricer.val.bg` - retrieves a **value** from the [**[Values]**](#Values) table called **bg**.
- `ricer.val.font_size` - retrieves a **value** from the [**[Values]**](#Values) table called **font_size**.
- `ricer.col.text` - retrieves a **color** from the [**[Colors]**](#Colors) table called **text** in it's **default format**.
- `ricer.col.outline.rgba01` - retrieves the **rgba01** value of a **color** from the [**[Colors]**](#Colors) table called **outline**.
- `ricer.col.background.r` - retrieves the **red** channel of a **color** from the [**[Colors]**](#Colors) table called **background**.
- `ricer.col.shadow.format(g01, rgba, hex, hb)` - retrieves the **red01** channel, **rgba** value, **hex** value and the **hex blue** channel of a **color** from the [**[Colors]**](#Colors) table called **shadow**.

*All color keywords can be found in the [**[Color Format]**](#Color-Format) section.*

## [Color Format]
**Color Format** is a string that can contain some of the following keywords:
- `hex`, `hexa`, `hr`, `hg`, `hb`, `ha`
- `rgb`, `rgba`, `r`, `g`, `b`, `a`
- `rgb01`, `rgba01`, `r01`, `g01`, `b01`, `a01`

All the keywords will be replaced when ricing the template with the rest of the string remaining the same.

# Using Ricer
Using Ricer is fairly straightforward.
Simply run Ricer `python Ricer.py` in your terminal, optionally pass your config path as an argument and enjoy your rice!
If you have any questions, feel free to contact me on any platform found on [my website](https://nnra6864.github.io/nnra/)!

# Links
- ### [Ricer](https://nnra6864.github.io/nnra/?page=Projects&project=27) - Project page
- ### [Nord Config](https://github.com/nnra6864/Hyprnord/blob/Arch/Ricer/Nord.toml) - My Nord Config
- ### [Rice Bowl Icon](https://uxwing.com/rice-bowl-icon/) - Image I used for creating the icon
