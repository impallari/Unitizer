# Unitizer Plugin for Glyphs

This is a plugin for the [Glyphs font editor](http://glyphsapp.com/). After installation, it will add the menu item *View > Show Unitizer*.

It's useful for working in Unitized fonts. It display guidelines (correspondong to user defined units) in the background of the current glyph in Edit view.

![Showing Units in the background.](unitizer01.png "Showing Units in the background")

### Unitized fonts?

1. Add some text here explaining what "unitized fonts" are..

### Installation

1. Download the complete ZIP file and unpack it, or clone the repository.
2. Double click the .glyphsReporter file. Confirm the dialog that appears in Glyphs.
3. Restart Glyphs

### Usage Instructions

1. In *Font Info > Masters* add custom parameter named *unitizerUnit* and set a value of your preference. (*10*, *12*, *20* or whatever value you want your unit to be).
2. Open a glyph in Edit View.
3. Use *View > Show Unitizer* to toggle the display of guidelines, according to your *unitizerUnit* custom parameter value.
4. If the advance width of your current glyph does not fit in your unit scheme, the difference will be shown in red.

### Requirements

The plugin works in the latest version of Glyphs.

### License

Copyright 2016 Pablo Impallar (@impallari).
Based on sample code by Rainer Erich Scheichelbauer (@mekkablue).

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

See the License file included in this repository for further details.